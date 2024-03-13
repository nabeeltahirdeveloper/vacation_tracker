#!/usr/bin/python3
"""This is the Employment model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, DateTime, ForeignKey

class Employment(BaseModel, Base):
  """class Employment with different ATTS"""
  __tablename__ = 'employments'
  starts_at = Column(DateTime, nullable=False)
  ends_at = Column(DateTime, nullable=True)
  user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
