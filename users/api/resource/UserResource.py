from flask import jsonify, make_response
from flask_restful import Resource
from users.api.controller.UserController import Controller
from config import token_is_valid, ExpiredSignatureError

controller=Controller()


class UserRegister(Resource):
    """
    class User Register will have only post method, where it will add user data into database
    """
    def post(self):
        try:
            response=controller.do_register()
            return make_response(response)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)
        

class UserResource(Resource):
    """
    class UserResource will have patch, get and delete methods to handle various operations over user data
    """
    
    def get(self):
        """
        Get all the users data
        Token is required to access get method
        """
        try:
            token_is_valid()
            response=controller.get_all_users()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)
        

    def patch(self):
        """
        Update user data
        Token is required
        """
        try:
            token_is_valid()
            response=controller.do_patch()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)
        
    
    def delete(self): 
        """
        Delete user data from database
        Token is required
        """  
        try:
            token_is_valid()
            response=controller.do_delete()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)


class UserLoginResource(Resource):
    """
    class UserLoginResourece will have only post method, where it will handle user login process
    return access token
    """
    def post(self):
        try:
            response=controller.do_login()
            return make_response(response)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)