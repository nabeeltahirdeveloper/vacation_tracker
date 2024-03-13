#!/usr/bin/python3
"""View for User objects that handles all default RestFul API actions"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage
#from api.v1.views.auth import authenticate, authorize

@app_views.route("/register", methods=["POST"], strict_slashes=False)
def register_user():
  """Tested user for testing the registration process while authentication and authorization"""
  data = request.json
  if not data:
    return jsonify({"error": "Missing user data"}), 400
  
  # extract user info from data 
  user_email = data.get("email")
  username = data.get("first_name")
  
  # validation for missing fields
  if not user_email or not username:
        return jsonify({"error": "Both first_name and email are required"}), 400

  # check if user already exists - in this case we can assign an exited user to rgister with 
  existed_user = storage.get_user_by_name(user_email)
  if existed_user:
    return jsonify({"error": "Username already exists"}), 409
  

  #create new user - in this case we will need to create a new user with all aspects as we did in the python session
  new_user = User(first_name="Hossam", last_name="Youssef", email="rita@example.com", personal_email="r.john@example.com", national_id_number="12345678910123", personal_phone="12345678910123", phone="12345678910123", title="Software Engineer")
  new_user.save()
  return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['GET'])
#@authenticate
#@authorize('super admin')
def get_user_id(user_id):
  """Retrieves a specific User object"""
  user = storage.get(User, user_id)
  if user is None:
    abort(404)
  return jsonify(user.to_dict())

@app_views.route("/users", strict_slashes=False, methods=['GET'])
#@authenticate
#@authorize('super admin')
def get_users():
  """retrieves all users"""
  users_list = []
  users = storage.all(User)
  for user in users.values():
    users_list.append(user.to_dict())
  return jsonify(users_list)

@app_views.route("/users/<user_id>", strict_slashes=False, methods=['DELETE'])
#@authenticate
#@authorize('super admin')
def delete_user_id(user_id):
  """deletes a specific user object"""
  user = storage.get(User, user_id)
  if user is None:
    abort(404)
  storage.delete(user)
  storage.save()
  print("User has been successfully deleted")
  return jsonify({}), 200
  
@app_views.route("/users", strict_slashes=False, methods=['POST'])
#@authenticate
#@authorize('super admin')
def post_user():
  """Creates a new user"""
  data = request.get_json()
  if not data:
    abort(400, "Not a JSON")
  if 'first_name' not in data.keys():
    abort(400, "Missing first_name")
  if 'last_name' not in data.keys():
    abort(400, "Missing last_name")
  if 'email' not in data.keys():
    abort(400, "Missing email")
  # if 'password' not in data.keys():
  #   abort(400, "Missing password")
  if 'personal_email' not in data.keys():
    abort(400, "Missing personal_email")
  if 'national_id_number' not in data.keys():
    abort(400, "Missing national_id_number")
  if 'personal_phone' not in data.keys():
    abort(400, "Missing personal_phone")
  if 'phone' not in data.keys():
    abort(400, "Missing phone")
  if 'title' not in data.keys():
    abort(400, "Missing title")
  # if 'head_user_id' not in data.keys():
  #   abort(400, "Missing head_user_id")
  if 'unit_id' not in data.keys():
    abort(400, "Missing unit_id")

  new_user = User(**data)
  new_user.save()
  return jsonify(new_user.to_dict()), 201

@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
#@authenticate
#@authorize('super admin')
def put_user(user_id):
  """edit in a specific user by its ID"""
  data = request.get_json()
  if not data:
    abort(400, "Not a JSON")
  updated_user = storage.get(User, user_id)
  if updated_user is None:
    abort(404)

  for key, value in data.items():
    if key not in ['id', 'email', 'created_at', 'updated_at']:
      setattr(updated_user, key, value)
  storage.save()
  return jsonify(updated_user.to_dict()), 200
