import os
from sqlalchemy import text
from flask import make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError

SCHEMA_NAME = os.getenv('DB_SCHEMA')
REGISTER_REQUIRED_FIELDS=os.getenv('REGISTER_FIELDS').split(',')
LOGIN_FIELDS=os.getenv('LOGIN_FIELDS').split(',')
BOOK_REQUIRED_FIELDS=os.getenv('BOOK_FIELDS').split(',')
BOOK_NAME=os.getenv('DELETE_BOOK_NAME').split(' ')

db=SQLAlchemy()
jwt=JWTManager()


def cli_commands(app):
    @app.cli.command('db_create')
    def db_create():
        """Create schema and tables in the database."""
        with app.app_context():
            # Create the schema if it doesn't exist
            db.session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"))
            print(f"Schema '{SCHEMA_NAME}' created or already exists.")
            db.session.commit()

        db.create_all()
        print('Database Created..')

    @app.cli.command('db_drop')
    def db_drop():
        with app.app_context():
            db.session.execute(text(f"DROP SCHEMA IF EXISTS {SCHEMA_NAME} CASCADE"))
            print(f"Schema '{SCHEMA_NAME}' Dropped.")
            db.session.commit()
        db.drop_all()
        print('Database Dropped')

@jwt_required()
def token_is_valid():pass