from app import db
from collections import Counter
from users.model.users import User
from flask import jsonify, request
from config import create_access_token, get_jwt_identity, jwt_required, token_is_valid, ExpiredSignatureError, REGISTER_REQUIRED_FIELDS

class Controller:

    def do_delete(self):
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form()
        email=data['email']
        password=data['password']

        try:    
            user=User.query.filter_by(email=email).first()
            if user:
                if User.query.filter_by(email=email, password=str(password)).first():
                    User.query.filter_by(email=email).delete()
                    db.session.commit()
                    return jsonify(message='User Data Removed Successfully '),200
                else:
                    return jsonify(message='Username and Password Mismatch'),401
            else:
                return jsonify(message='User Not Available !'),404
        except Exception as e:
            return jsonify(message=f'Exception Occurred, Exception Message = {e}'),400
    
    def do_patch(self):
        if request.is_json:
            data=request.get_json()
            update_dict={i:data[i] for i in data.keys()}    
        else:
            data=request.form()
            update_dict={i:data[i] for i in data.keys()}
        update_dict.update({"modified_by":get_jwt_identity()})
        
        try:  
            user=User.query.filter_by(email=data['email']).first()
            if user:
                User.query.filter_by(email=data['email']).update(update_dict)
                db.session.commit()
                return jsonify(message='User data modified successfully '),200
            else:
                return jsonify(message='User Not Available!, Please verify email id.'),404
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
            data=request.form()
            
        if Counter(REGISTER_REQUIRED_FIELDS)!=Counter(data.keys()):
            return jsonify(message=f'Required Fields = {''.join(REGISTER_REQUIRED_FIELDS)}'),400
        
        first_name=data['first_name']
        last_name=data['last_name']
        email=data['email']
        password=data['password']
        
        try:
            user=User.query.filter_by(email=email).first()
            if user:
                return jsonify(message='User already exist'),409
            else:
                db.session.add(User(first_name=first_name, last_name=last_name, email=email, password=password))
                db.session.commit()
                return jsonify(message='User Successfully Created!'),201
        except Exception as e:
            return jsonify(message=f'Exception Occurred, Exception Message = {e}'),400
    
    def do_login(self):
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form()
        email=data['email']
        password=data['password']

        try:
            mailid=User.query.filter_by(email=email, password=str(password)).first()
            if mailid:
                access_token=create_access_token(identity=email)
                return jsonify(message='Login Successful', access_token=access_token),200
            else:
                return jsonify(message='Invalid Username or Password'),401
        except Exception as e:
            return jsonify(message=f'Exception Occurred, Exception Message = {e}'),400