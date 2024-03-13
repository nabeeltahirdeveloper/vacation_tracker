#!/usr/bin/python3
"""View for User objects that handles all default RestFul API actions"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.employment import Employment
from models import storage
from datetime import datetime

@app_views.route("/employments/<user_id>", strict_slashes=False, methods=['GET'])
def get_employment_id(user_id):
  """Retrieves a specific Employment object"""
  employment = storage.get(Employment, user_id)
  if employment is None:
    abort(404)
  return jsonify(employment.to_dict())

@app_views.route("/employments", strict_slashes=False, methods=['GET'])
def get_employments():
  """retrieves all the employments"""
  employments_list = []
  employments = storage.all(Employment)
  for employment in employments.values():
    employments_list.append(employment.to_dict())
  return jsonify(employments_list)
"""retrieves all the employement dates"""

@app_views.route("/employments/<emp_id>", strict_slashes=False, methods=['DELETE'])
def delete_employment_id(emp_id):
  """deletes a specific employement date"""
  emp_obj = storage.get(Employment, emp_id)
  if emp_obj is None:
    abort(404)
  storage.delete(emp_obj)
  storage.save()
  print("Employment has been successfully deleted")
  return jsonify({}), 200

@app_views.route("/employments", strict_slashes=False, methods=['POST'])
def post_emp_date():
  """Creates a new Employment date"""
  data = request.get_json()
  if not data:
    abort(400, "Not a JSON")
  if 'starts_at' not in data.keys():
    abort(400, "Missing Designation date")
  # if 'ends_at' not in data.keys():  
  #   abort(400, "Missing Resignation date")
  new_employement = Employment(**data)
  new_employement.save()
  return jsonify(new_employement.to_dict()), 201

@app_views.route("/employments/<emp_id>", strict_slashes=False, methods=['PUT'])
def put_emp(emp_id):
  """edit in a specific user by its ID"""
  data = request.get_json()
  if not data:
    abort(400, "Not a JSON")
  updated_emp = storage.get(Employment, emp_id)
  if updated_emp is None:
    abort(404)

  for key, value in data.items():
    if key not in ['id', 'created_at', 'updated_at']:
      setattr(updated_emp, key, value)
  storage.save()
  return jsonify(updated_emp.to_dict()), 200
