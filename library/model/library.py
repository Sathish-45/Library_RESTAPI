from sqlalchemy import Column, Integer, String, DateTime, Sequence
from sqlalchemy.sql import func
from app import db


class BookData(db.Model):
    __tablename__='book_data'
    __table_args__ = {'schema': 'library'}

    id=Column(Integer,Sequence('book_id',start=1,increment=1), primary_key=True, autoincrement=True, unique=True)
    book_name=Column(String(30), unique=True)
    author=Column(String(30))
    book_price=Column(Integer)
    created_date=Column(DateTime,default=func.now())
    last_updated=Column(DateTime,onupdate=func.now())
    modified_by=Column(String(30))

    def to_dict(self):
        return {
            "book_name": self.book_name,
            "author": self.author,
            "book_price": self.book_price,
            "created_date":self.created_date,
            "last_updated":self.last_updated,
            "modified_by":self.modified_by
        }
