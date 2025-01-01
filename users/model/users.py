from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.sql import func
from app import db


class User(db.Model):
    __tablename__='user'
    __table_args__ = {'schema': 'library'}

    id=Column(Integer, Sequence('user_id',start=1,increment=1), primary_key=True, autoincrement=True, unique=True)
    first_name=Column(String(30))
    last_name=Column(String(30))
    email=Column(String(40), unique=True)
    password=Column(String(20))
    created_date=Column(DateTime,default=func.now())
    last_updated=Column(DateTime,onupdate=func.now())
    modified_by=Column(String(30))

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_date":self.created_date,
            "last_updated":self.last_updated,
            "modified_by":self.modified_by
        }
