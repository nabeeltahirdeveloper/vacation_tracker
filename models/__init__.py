#!/usr/bin/python3
"""This module instantiates an abject of a class db storage"""
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.employment import Employment
from models.request import Request
from models.unit import Unit

storage = DBStorage()
storage.reload()
