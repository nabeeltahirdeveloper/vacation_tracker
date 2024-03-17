#!/usr/bin/python3
"""This is the User model"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class LeaveRequest(BaseModel, Base):
  """class User with different ATTS"""
  __tablename__ = 'leave_requests'
  user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
  start_date = Column(String(60), nullable=False)
  end_date = Column(String(60), nullable=False)
  status = Column(String(60), nullable=False)
  leave_days = Column(String(60), nullable=False)
  manager_id = Column(String(60), ForeignKey('users.id'), nullable=True)
  

  
  def is_active(self):
    """is_active"""
    return True
  
  def get_id(self):
    """get_id"""
    return self.email
  
  def is_authenticated(self):
    """is_authenticated"""
    return True
