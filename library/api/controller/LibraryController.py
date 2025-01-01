from app import db
from library.model.library import BookData
from flask import jsonify, request
from config import create_access_token, get_jwt_identity, jwt_required, token_is_valid, ExpiredSignatureError


class Controller:

    def get_books(self, name=None):
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
        name=request.form.get('book_name')
        author=request.form.get('author')
        price=request.form.get('price')
        if not name or not author or not price:
            return jsonify(message='Please fill all required fields'),400
        exists=BookData.query.filter_by(book_name=name).first()
        if exists:
            BookData.query.filter_by(book_name=name).update({"author":author,"book_price":price,"modified_by":get_jwt_identity()})
            db.session.commit()
            return jsonify(message=f'{name} Book Already Available. Hence data updated'),200
        else:
            data=BookData(book_name=name, author=author, book_price=price)
            db.session.add(data)
            db.session.commit()
            return jsonify(message='Book added to library'),200