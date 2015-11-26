#-*-coding:utf-8-*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import json

Base = declarative_base()


class Department(Base): #조직
  __tablename__ = 'department'
  dept_code = Column(String(4), primary_key=True)
  dept_desc = Column(String(30))
  d_o = relationship("Dept_obj", backref="department")
#조직(department)과 조직목표(dept_obj)는 one to many관계
#조직(department)은 조직내(department.d_o)를 이용해서 조직목표 클레스(Dept_obj)객체 참조가 가능하다.
#또한 조직목표 클레스(Dept_obj)객체도 조직(department)을 참조 가능하다.

#조직목표
class Dept_obj(Base):
  __tablename__ = 'dept_obj'
  dept_code = Column(String(4), ForeignKey('department.dept_code'), primary_key=True)
  obj_code = Column(String(3), ForeignKey('object.obj_code'), primary_key=True)
  dept_obj_resp = Column(String(1))
  dept_obj_auth = Column(String(1))
  dept_obj_exp = Column(String(1))
  dept_obj_work = Column(String(1))
  dept_obj_ref = Column(String(1))

#목표
class Object(Base):
  __tablename__ = 'object'
  obj_code = Column(String(3), primary_key=True)
  obj_desc = Column(String(40))
  obj_priority = Column(Integer(2))
  d_ob = relationship("Dept_obj", backref="object")

engine = create_engine("mysql://root:wjdtnsgud1!@localhost/isp", encoding='utf8', echo=True)
Base.metadata.create_all(engine)
