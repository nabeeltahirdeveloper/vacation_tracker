#!/usr/bin/python3
"""View for VacationRequest objects that handles all default RestFul API actions"""

from api.v1.views import app_views
from models import storage, Unit, User, Employment, Request
from flask import Flask, Blueprint, jsonify, request, make_response, abort

@app_views.route('/units/<unit_id>/requests', strict_slashes=False, methods=['GET'])
def vacation_req_response_by(unit_id):
    """Retrieves all the vacation requests by unit"""
    unit = storage.get(Unit, unit_id)
    if unit is None:
        abort(404)
    req_list = []
    for user in unit.users:
        for emp in user.employments:
            for req in emp.requests:
                req_list.append(req.to_dict())
    return jsonify(req_list)

# @app_views.route('/users/<user_id>/requests', strict_slashes=False, methods=['GET'])
# def vacation_req_responseuser_by(user_id):
#     """Retrieves all the vacation requests by the Head_user_id or by the  user himself"""
#     user = storage.get(User, user_id)
#     if user is None:
#         abort(404)
#     req_list = []
    

@app_views.route('/employments/<emp_id>/requests', strict_slashes=False, methods=['GET'])
def vacation_req_responseemploy_by(emp_id):
    """Retrieves all the vacation requests by the Employment_id"""
    emp = storage.get(Employment, emp_id)
    if emp is None:
        abort(404)
    req_list = []
    for req in emp.requests:
        req_list.append(req.to_dict())
    return jsonify(req_list)

@app_views.route('/requests', strict_slashes=False, methods=['GET'])
def get_requests():
    """Retrieves all the vacation requests"""
    req_list = []
    requests = storage.all(Request)
    for req in requests.values():
        req_list.append(req.to_dict())
    return jsonify(req_list)

@app_views.route('/requests/<req_id>', strict_slashes=False, methods=['GET'])
def get_request(req_id):
    """Retrieves a specific vacation request"""
    req = storage.get(Request, req_id)
    if req is None:
        abort(404)
    return jsonify(req.to_dict())

@app_views.route('/requests', strict_slashes=False, methods=['POST'])
def post_request():
    """Creates a new vacation request"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")
    if 'duration' not in data.keys():
        abort(400, "Missing duration")
    if 'response_by_id' not in data.keys():
        abort(400, "Missing Manager Approval")
    if 'response' not in data.keys():
        abort(400, "Missing response status")
    if 'starts_at' not in data.keys():
        abort(400, "Missing starts_at date")
    if 'ends_at' not in data.keys():
        abort(400, "Missing ends_at date")
    new_request = Request(**data)
    new_request.save()
    return jsonify(new_request.to_dict()), 201

@app_views.route('/requests/<req_id>', strict_slashes=False, methods=['PUT'])
def put_request(req_id):
    """edit in a specific vacation request by its ID"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    updated_req = storage.get(Request, req_id)
    if updated_req is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(updated_req, key, value)
    storage.save()
    return jsonify(updated_req.to_dict()), 200

@app_views.route('/requests/<req_id>', strict_slashes=False, methods=['DELETE'])
def delete_request(req_id):
    """deletes a specific vacation request by its ID"""
    req_obj = storage.get(Request, req_id)
    if req_obj is None:
        abort(404)
    storage.delete(req_obj)
    storage.save()
    print("vacation request has been deleted successfully")
    return jsonify({}), 200
