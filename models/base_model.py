#!/usr/bin/python3
"""This module is defining  a base model for all models in the app"""
import uuid
import models
from datetime import datetime
from sqlalchemy import Integer, String, Column, DateTime, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class BaseModel:
    """This class is defining  a base model for all models in the app"""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    
    def __init__(self, *args, **kwargs):
      """Base Model Insialization"""
      if kwargs:
        if 'id' not in kwargs:
          self.id = str(uuid.uuid4())
        if 'created_at' not in kwargs:
          self.created_at = datetime.utcnow()
        if 'updated_at' not in kwargs:
          self.updated_at = datetime.utcnow()
        if '__class__' in kwargs:
          del kwargs['__class__']
        for key, value in kwargs.items():
          setattr(self, key, value)
      else:
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def __str__(self):
      """String Representation"""
      return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
      """This method to save the base model"""
      self.updated_at = datetime.utcnow()
      models.storage.new(self)
      models.storage.save()

    def delete(self):
      """This method to delete the base model"""
      models.storage.delete(self)

    def to_dict(self):
      """This method to return a dictionary representation of the base model"""
      dictionary = dict(self.__dict__)
      if "_sa_instance_state" in dictionary:
        del dictionary["_sa_instance_state"]
      dictionary["created_at"] = self.created_at.isoformat()
      dictionary["updated_at"] = self.updated_at.isoformat()
      return dictionary