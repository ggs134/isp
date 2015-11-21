from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Department(Base):
  __tablename__ = 'department'
  dept_code = Column(char(4), primary_key=True)
  dept_desc = Column(varchar(30))
  dept = relationship("Dept_obj", backref="department")


class Object(Base):
  __tablename__ = 'object'
  obj_code = Column(char(3), primary_key=True)
  obj_desc = Column(varchar(40))
  obj_priority = Column(number(2))
  obj = relationship("Dept_obj", backref="object")


class Dept_obj(Base):
  __tablename__ = 'dept_obj'
  dept_code = Column(char(4), ForeignKey('department.dept_code'), primary_key=True)
  obj_code = Column(char(3), ForeignKey('object.obj_code'), primary_key=True)
  dept_obj_resp = Column(char(1))
  dept_obj_auth = Column(char(1))
  dept_obj_exp = Column(char(1))
  dept_obj_work = Column(char(1))
  dept_obj_ref = Column(char(1))

engine = create_engine("mysql://root:1127@localhost/isp", encoding='utf8', echo=True)
Base.metadata.create_all(engine)
