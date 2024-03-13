#!/usr/bin/python3
"""This is the Request model"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, Integer

class Request(BaseModel, Base):
  """Class Request"""
  __tablename__ = 'requests'
  user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
  note = Column(String(500), nullable=True)
  starts_at = Column(DateTime, nullable=False)
  ends_at = Column(DateTime, nullable=False)
  duration = Column(Integer, nullable=False)
  response_by_id = Column(String(60), ForeignKey('users.id'), nullable=True)
  response = Column(Boolean, nullable=True)
  response_note = Column(String(1000), nullable=True)
