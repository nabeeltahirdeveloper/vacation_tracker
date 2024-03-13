#!/usr/bin/python3
"""View for Unit objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import Unit, User
from flask import Flask, Blueprint, jsonify, request, make_response, abort
from models import storage

@app_views.route("/units/<unit_id>/users", strict_slashes=False, methods=['GET'])
def get_users_by_unit(unit_id):
    """Retrieves all the users by unit"""
    unit = storage.get(Unit, unit_id)
    if unit is None:
        abort(404)
    users_list = []
    for user in unit.users:
        users_list.append(user.to_dict())
    return jsonify(users_list)

@app_views.route("/units/<unit_id>", strict_slashes=False, methods=['GET'])
def get_unit_id(unit_id):
    """Retrieves a specific Unit object"""
    unit = storage.get(Unit, unit_id)
    if unit is None:
        abort(404)
    return jsonify(unit.to_dict())
  
@app_views.route("/units", strict_slashes=False, methods=['GET'])
def get_units():
    """retrieves all units"""
    units_list = []
    units = storage.all(Unit)
    for unit in units.values():
        units_list.append(unit.to_dict())
    return jsonify(units_list)

@app_views.route("/units/<unit_id>", strict_slashes=False, methods=['DELETE'])
def delete_unit_id(unit_id):
    """deletes a specific unit object"""
    unit = storage.get(Unit, unit_id)
    if unit is None:
        abort(404)
    storage.delete(unit)
    storage.save()
    print("Unit has been successfully deleted")
    return jsonify({}), 200

@app_views.route("/units", strict_slashes=False, methods=['POST'])
def post_unit():
    """Creates a new unit"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(400, "Missing name")
    new_unit = Unit(**data)
    new_unit.save()
    return jsonify(new_unit.to_dict()), 201

@app_views.route("/units/<unit_id>", strict_slashes=False, methods=['PUT'])
def put_unit(unit_id):
    """edit in a specific unit by its ID"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    updated_unit = storage.get(Unit, unit_id)
    if updated_unit is None:
        abort(404)

    for key, value in data.items():
        setattr(updated_unit, key, value)
    storage.save()
    return jsonify(updated_unit.to_dict()), 200
