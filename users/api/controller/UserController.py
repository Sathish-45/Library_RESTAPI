import re
from app import db
from collections import Counter
from users.model.users import User
from flask import jsonify, request
from email_validator import validate_email,EmailNotValidError
from config import create_access_token, get_jwt_identity, REGISTER_REQUIRED_FIELDS, LOGIN_FIELDS

class Controller:
    """
    class Contoller will have all the methods that are used by User Resource class
    """
    def validate_password(self, password):
        if len(password) < 8 or len(password) > 20:
            return "Password must be between 8 and 20 characters long."
        if not re.search(r'[A-Z]', password):
            return "Password must contain at least one uppercase letter."
        if not re.search(r'[a-z]', password):
            return "Password must contain at least one lowercase letter."
        if not re.search(r'\d', password):
            return "Password must contain at least one digit."
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return "Password must contain at least one special character."
        if re.search(r'\s', password):
            return "Password must not contain spaces."
        return True

    def email_is_valid(self,email):
        try:
            validate_email(email)
            return True
        except Exception as e:
            return str(e)


    def do_delete(self):
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form

        if Counter(LOGIN_FIELDS)!=Counter(data.keys()):
            return jsonify(message=f'Required Fields = {','.join(LOGIN_FIELDS)}'),400  

        email=data['email']
        password=data['password'] 
        
        user=User.query.filter_by(email=email).first()
        if user:
            if User.query.filter_by(email=email, password=str(password)).first():
                User.query.filter_by(email=email).delete()
                db.session.commit()
                return jsonify(message=f'User linked with {email} Mail id Removed Successfully '),200
            else:
                return jsonify(message='Username and Password Mismatch'),401
        else:
            return jsonify(message=f'User linked with {email} is Not Available !'),404


    def do_patch(self):
        if request.is_json:
            data=request.get_json()
            update_dict={i:data[i] for i in data.keys()}    
        else:
            data=request.form
            update_dict={i:data[i] for i in data.keys()}      
        try: 
            if 'email' in data.keys():
                valid_email=self.email_is_valid(data['email'])
                if valid_email != True:
                    return jsonify(message=valid_email),400
                
            if 'password' in data.keys():
                password_is_valid=self.validate_password(str(data['password']))
                if password_is_valid != True:
                    return jsonify(message=password_is_valid), 401

            update_dict.update({"modified_by":get_jwt_identity()})
            user=User.query.filter_by(email=data['email']).first()
            if user:
                User.query.filter_by(email=data['email']).update(update_dict)
                db.session.commit()
                return jsonify(message=f'{data['email']} data modified successfully '),200
            else:
                return jsonify(message=f'User with Mail id - {data['email']} Not Available!, Please verify email id.'),404
        except Exception as e:
            return jsonify(message=f'Exception Occurred, Exception Message = {e}'),400
    
    def get_all_users(self):
        try:
            users=User.query.all()
            serialized_users = [user.to_dict() for user in users]
            if users:
                return jsonify(serialized_users), 200
            else:
                return jsonify(message='No User Found'),404
        except Exception as e:
            return jsonify(message=f'Exception Occurred, Exception Message = {e}'),400
         
    def do_register(self):
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form
        
        if Counter(REGISTER_REQUIRED_FIELDS)!=Counter(data.keys()):
            return jsonify(message=f'Required Fields = {','.join(REGISTER_REQUIRED_FIELDS)}'),400
        
        first_name=data['first_name']
        last_name=data['last_name']
        email=data['email']
        password=str(data['password'])
        
        try:
            valid_email=self.email_is_valid(email)
            if valid_email != True:
                return jsonify(message=valid_email),400
            password_is_valid=self.validate_password(password)
            if password_is_valid != True:
                return jsonify(message=password_is_valid), 401
            user=User.query.filter_by(email=email).first()
            if user:
                return jsonify(message=f'User with Mail id - {email} already exist'),409
            else:
                db.session.add(User(first_name=first_name, last_name=last_name, email=email, password=password))
                db.session.commit()
                return jsonify(message=f'User with {email} mail id Successfully Created!'),201
        except Exception as e:
            return jsonify(message=f'Exception Occurred, Exception Message = {e}'),400
    

    def do_login(self):
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form

        if Counter(LOGIN_FIELDS)!=Counter(data.keys()):
            return jsonify(message=f'Required Fields = {','.join(LOGIN_FIELDS)}'),400 
        
        email=data['email']
        password=str(data['password'])

        try:
            valid_email=self.email_is_valid(email)
            if valid_email != True:
                return jsonify(message=valid_email),400
            password_is_valid=self.validate_password(password)
            if password_is_valid != True:
                return jsonify(message=password_is_valid), 401
            mailid=User.query.filter_by(email=email, password=password).first()
            if mailid:
                access_token=create_access_token(identity=email)
                return jsonify(message='Login Successful', access_token=access_token),200
            else:
                return jsonify(message='Invalid Username or Password'),401
        except Exception as e:
            return jsonify(message=f'Exception Occurred, Exception Message = {e}'),400