#!/usr/bin/python3
"""storage data engine
  MySQL DataBase
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.employment import Employment
from models.request import Request
from models.unit import Unit
import datetime

# Create a connection to the database using SQLAlchemy's ORM

classes = {"User": User, "Employment": Employment, "Request": Request, "Unit": Unit}

# Connect to Database and create a database session

class DBStorage:
  """DB engine class"""
  __engine = None
  __session = None

  def __init__(self):
    """Constructor method"""
    self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                  .format(getenv('VACATION_TRACKER_MYSQL_USER'),
                                          getenv('VACATION_TRACKER_MYSQL_PWD'),
                                          getenv('VACATION_TRACKER_HOST'),
                                          getenv('VACATION_TRACKER_DB')),
                                  pool_pre_ping=True)
    if getenv('VACATION_TRACKER_ENV') == 'test':
      Base.metadata.drop_all(self.__engine)

  def all(self, cls=None):
    """querying all the current objects in the session"""
    new_dict = {}
    for clss in classes:
      if cls is None or cls is classes[clss] or cls is clss:
        objs = self.__session.query(classes[clss]).all()
        for obj in objs:
          key = obj.__class__.__name__ + '.' + obj.id
          new_dict[key] = obj
    return (new_dict)

  def new(self, obj):
    """add the object to the current database session"""
    self.__session.add(obj)
    self.__session.flush()

  def save(self):
    """commit all changes of the current database session"""
    self.__session.commit()

  def delete(self, obj=None):
    """delete from the current database session obj if not None"""
    if obj is not None:
      self.__session.delete(obj)

  def reload(self): #what does this method do ?
    """create all tables in the database"""
    Base.metadata.create_all(self.__engine)
    session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    Session = scoped_session(session_factory)
    self.__session = Session()

  def close(self):
    """call remove() method on the private session attribute"""
    self.__session.close()

  def get(self, cls, id): #what does this method do ?
    """retrieves one object from the session and None if not found by id"""
    if cls in classes.values() and id and type(id) is str:
      dict_obj = self.all(cls)
      for key, value in dict_obj.items():
        if key.split('.')[1] == id:
          return value
    return None
  
  def count(self, cls=None):
    """returns number of objects in storage matching the given class.
        if no class count number of all objects in storage"""
    if cls:
      return len(self.all(cls))
    return len(self.all())

  def get_user_by_name(self, first_name):
    """Retrieves a user with the first_name from DB just for testing purposes"""
    for obj in self.all(User).values():
      if obj.first_name == first_name:
        return obj
    return None
