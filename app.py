import os
from flask import Flask,jsonify,make_response
from config import db, jwt
from flask_restful import Api
from config import cli_commands
from library.api.resource.LibraryResource import LibraryResource, GetBookByName
from users.api.resource.UserResource import UserResource, UserLoginResource, UserRegister

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']=os.getenv('JWT_SECRET_KEY')

cli_commands(app)
    
api=Api(app)
db.init_app(app)
jwt.init_app(app)


# Routes
api.add_resource(UserRegister,'/register')
api.add_resource(UserLoginResource,'/login')
api.add_resource(UserResource, '/users')
api.add_resource(LibraryResource, '/library')
api.add_resource(GetBookByName, '/library/book_name')


if __name__=='__main__':
    app.run(debug=True)