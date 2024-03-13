#!/usr/bin/python3
"""This is the Unit model"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class Unit(BaseModel, Base):
  """
  Represents a unit in the vacation tracker web application.
  This class provides the necessary attributes and methods to manage units.
  """
  __tablename__ = 'units'
  ancestry = Column(String(60), default='/', nullable=False)
  name = Column(String(60), nullable=False)
  head_user_id = Column(String(60), ForeignKey('users.id'), nullable=True)

  #relations
  users = relationship("User", backref="unit", foreign_keys="User.unit_id")
  head_user = relationship("User", uselist=False, backref="unit_head", foreign_keys=[head_user_id])
