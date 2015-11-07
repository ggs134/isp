from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base=declarative_base()


app =Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:wjdtnsgud1!@localhost/annonymous?charset=utf8'
# db=SQLAlchemy(app)

class Entries(Base):
	__tablename__='entries'
	id=Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	title=Column(String(200), unique=True)
	text=Column(String(1000),unique=True)

class Board1(Base):
	__tablename__='board1'
	id=Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	title=Column(String(200), unique=True)
	text=Column(String(1000),unique=True)

class Board2(Base):
	__tablename__='board2'
	id=Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	title=Column(String(200), unique=True)
	text=Column(String(1000),unique=True)

engine=create_engine("mysql://root:wjdtnsgud1!@localhost/annonymous", encoding='utf8', echo=True)

Base.metadata.create_all(engine)
