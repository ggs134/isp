from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Organization(Base):
  __tablename__ = 'organization'
  organization_num = Column(Integer, primary_key=True)
  supraorganizaion_name = Column(String(50))
  subedifice_name = Column(String(50))
  o_g_n = relationship("Organization_goal", backref="organization")


class Goal(Base):
  __tablename__ = 'goal'
  goal_num = Column(Integer, primary_key=True)
  originalgoal_name = Column(String(50))
  subgoal_name = Column(String(50))
  g_n = relationship("Organization_goal", backref="goal")


class Organization_goal(Base):
  __tablename__ = 'organization_goal'
  organization_num = Column(Integer, ForeignKey('organization.organization_num'), primary_key=True)
  goal_num = Column(Integer, ForeignKey('goal.goal_num'), primary_key=True)
  importance = Column(String(2))

engine = create_engine("mysql://root:rlagnlrud@52.192.98.130/isptest", encoding='utf8', echo=True)
Base.metadata.create_all(engine)



