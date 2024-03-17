#!/usr/bin/python3
"""This is the User model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class User(BaseModel, Base):
  """class User with different ATTS"""
  __tablename__ = 'users'
  first_name = Column(String(130), nullable=False)
  last_name = Column(String(130), nullable=False)
  email = Column(String(130), nullable=False)
  password = Column(String(130), nullable=False)
  personal_email = Column(String(130), nullable=False)
  national_id_number = Column(String(14), nullable=False)
  personal_phone = Column(String(14), nullable=False)
  phone = Column(String(14), nullable=False)
  title = Column(String(130), nullable=False)
  user_role = Column(String(130), nullable=False)
  yearly_leave = Column(String(130), default=21, nullable=False)
  #head_user_id = Column(String(14), nullable=False)
  unit_id = Column(String(60), ForeignKey('units.id'), nullable=False)
  head_user_id = Column(String(60), ForeignKey('users.id'), nullable=True)
  
  def is_active(self):
    """is_active"""
    return True
  
  def get_id(self):
    """get_id"""
    return self.email
  
  def is_authenticated(self):
    """is_authenticated"""
    return True
