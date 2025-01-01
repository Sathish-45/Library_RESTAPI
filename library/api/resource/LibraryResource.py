from app import db
from flask import jsonify, request, make_response
from flask_restful import Resource
from library.model.library import BookData
from library.api.controller.LibraryController import Controller
from config import jwt_required, get_jwt_identity, token_is_valid, ExpiredSignatureError

controller=Controller()


class LibraryResource(Resource):
    
    #@jwt_required() #get all books
    def get(self):
        try:
            token_is_valid()
            response=controller.get_books()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)

         
    #@jwt_required() #add Book
    def post(self):
        try:
            token_is_valid()
            response=controller.post_books()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)

  
class GetBookByName(Resource):
    #@jwt_required()
    def get():
        try:
            token_is_valid()
            name=request.form.get('book_name')
            if name:
                response=controller.get_books(name=name)
                return make_response(response)
            else:
                return make_response(jsonify(message='Please provide book name'),404)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
    
