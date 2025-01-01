from app import db
from collections import Counter
from library.model.library import BookData
from flask import jsonify, request
from config import get_jwt_identity, BOOK_REQUIRED_FIELDS, BOOK_NAME


class Controller:

    def get_books(self, name=None):
        """
        Method will return all books/ based on book name
        """
        if name:
            books=BookData.query.filter_by(book_name=name)
        else:
            books=BookData.query.all()
        if books:
            serialized_data = [data.to_dict() for data in books]
            return jsonify(serialized_data), 200
        else:
            return jsonify(message='No Books Found'),404
    
    def post_books(self):
        """
        Method will accept both json and form data.
        Add books data into database
        """
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form
        
        if Counter(BOOK_REQUIRED_FIELDS)!=Counter(data.keys()):
            return jsonify(message=f'Please fill the all required fields, Required Fields = {','.join(BOOK_REQUIRED_FIELDS)}'),400

        name=data.get('book_name')
        author=data.get('author')
        price=data.get('book_price')
        
        exists=BookData.query.filter_by(book_name=name).first()
        if exists:
            update_dict={i:data[i] for i in data.keys()}
            update_dict.update({"modified_by":get_jwt_identity()})
            BookData.query.filter_by(book_name=name).update(update_dict)
            db.session.commit()
            return jsonify(message=f'{name} Book Already Available. Hence data updated'),200
        else:
            data=BookData(book_name=name, author=author, book_price=price)
            db.session.add(data)
            db.session.commit()
            return jsonify(message=f'{name} Book added to library'),200


    def do_delete(self):
        if request.is_json:
            data=request.get_json()
        else:
            data=request.form
        print(data.keys())
        if Counter(data.keys()) != Counter(BOOK_NAME):
            return jsonify(message=f'Please fill the Required Field = {','.join(BOOK_NAME)}'),400

        book_name=data['book_name']

        book=BookData.query.filter_by(book_name=book_name).first()
        if book:
            BookData.query.filter_by(book_name=book_name).delete()
            db.session.commit()
            return jsonify(message=f'{book_name} Book Removed Successfully '),200
        else:
            return jsonify(message=f'{book_name} Book Not Available !'),404
    