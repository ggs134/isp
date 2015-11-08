from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, String

Base = delclarative_base()


class Organization(Base):
  __tablename__ = 'organization'
  organization_num = column(Integer, primary_key=True)
  supraorganizaion_name = Column(String(50))
  subedifice_name = Column(String(50))
  o_g_n = relationship("Organization_goal", backref="organization")


class Goal(Base):
  __tablename__ = 'goal'
  goal_num = column(Integer, primary_key=True)
  originalgoal_name = Column(String(50))
  subgoal_name = Column(String(50))
  g_n = relationship("Organization_goal", backref="goal")


class Organization_goal(Base):
  __tablename__ = 'organization_goal'
  organization_num = column(Integer, ForeignKey('organization.organization_num'))
  goal_num = column(Integer, ForeignKey('goal.goal_num'))
  importance = Column(String(2))
