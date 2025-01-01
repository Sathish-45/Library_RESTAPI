from flask import jsonify, request, make_response
from flask_restful import Resource
from library.api.controller.LibraryController import Controller
from config import token_is_valid, ExpiredSignatureError

controller=Controller()


class LibraryResource(Resource):
    """
    class LibraryResource will have get , post and delete methods to handle required operations on book data
    All methods require valid token
    """
    
    def get(self):
        """
        Get all books
        """
        try:
            token_is_valid()
            response=controller.get_books()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)


    def post(self):
        """
        Post new book data into database
        """
        try:
            token_is_valid()
            response=controller.post_books()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)
    

    def delete(self):
        """
        delete book data based on book name
        """
        try:
            token_is_valid()
            response=controller.do_delete()
            return make_response(response)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)

  
class GetBookByName(Resource):
    """
    class GetBookByName will have only get method, where it will return book data based on book name
    Token validation is required
    """
    def get():
        try:
            token_is_valid()
            if request.is_json:
                data=request.get_json()
            else:
                data=request.form
                
            name=data.get('book_name')
            if name:
                response=controller.get_books(name=name)
                return make_response(response)
            else:
                return make_response(jsonify(message='Please provide book name'),404)
        except ExpiredSignatureError:
            return make_response(jsonify(message="Token has expired. Please log in again."), 401)
        except Exception as e:
            return make_response(jsonify(message=f'Exception Occurred, Exception Message = {e}'),400)
    
