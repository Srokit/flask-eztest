"""Test model"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

Base = declarative_base()


def init_db(app):
    db.init_app(app)
    with app.app_context():
        Base.metadata.create_all(db.engine)


class Table1(Base):
    __tablename__ = 'table1'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))


class Table2(Base):
    __tablename__ = 'table2'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    number = Column(Integer)