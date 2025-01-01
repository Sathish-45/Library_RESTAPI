from app import db
from flask import jsonify, request, make_response
from flask_restful import Resource
from users.model.users import User
from users.api.controller.UserController import Controller
from config import create_access_token, get_jwt_identity, jwt_required, token_is_valid, ExpiredSignatureError

controller=Controller()

class UserRegister(Resource):
    def post(self): #Register
        response=controller.do_register()
        return make_response(response)
    

class UserResource(Resource):
    
    def get(self): #Get all users
        try:
            token_is_valid()
            response=controller.get_all_users()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)

    #@jwt_required()
    def patch(self): # Updated user details
        try:
            token_is_valid()
            response=controller.do_patch()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
    
    def delete(self): # delete user details   
        try:
            token_is_valid()
            response=controller.do_delete()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)


class UserLoginResource(Resource):
    def post(self): #Login
        response=controller.do_login()
        return make_response(response)