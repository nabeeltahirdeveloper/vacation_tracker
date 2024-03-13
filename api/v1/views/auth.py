#!/usr/bin/python3
"""authenticate and authorize decorators. The authenticate decorator ensures that the user is authenticated, 
while the authorize decorator checks if the authenticated user has the 'admin' permission. If both checks pass, 
the endpoint handler is executed; otherwise, an appropriate error response is returned."""

from functools import wraps
from flask import request, jsonify
from models import storage, User

def authenticate(func):
    """authenticate decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """wrapper function - # Check if user is authenticated (e.g., by validating authentication token)"""
        auth = request.authorization
        if auth is None:
            return jsonify({"error": "Unauthorized - Authentication is Needed"}), 401

        user = storage.get(User, request.authorization.username)
        if user is None or not user.is_valid_password(request.authorization.password):
            return jsonify({"error": "Unauthorized"}), 401

        return func(*args, **kwargs)
    return wrapper

def authorize(role):
    """authorize decorator - # Check if user is a super admin with the needed permissions"""
    def decorator(func):
      @wraps(func)
      def wrapper(*args, **kwargs):
        """wrapper function - Check if user is authorized as a super admin"""
        if request.authorization is None:
            return jsonify({"error": "Unauthorized User - Authentication is Needed"}), 401

        user = storage.get(User, request.authorization.username)
        if user is None or not user.is_valid_password(request.authorization.password):
            return jsonify({"error": "Unauthorized User"}), 401

        if user.role != "super admin":
          return jsonify({"error": " Forbidden- Not a Super Admin User"}), 401
        return func(*args, **kwargs)
      return wrapper
    return decorator

# def authorize(role):
#     """authorize decorator - # Check if user is authorized with the needed permissions"""
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             """wrapper function - Check if user is authorized with the needed permissions"""
#             if request.authorization is None:
#                 return jsonify({"error": "Unauthorized - Authentication is Needed"}), 401
#             user = storage.get(User, request.authorization.username)
#             if user is None or not user.is_valid_password(request.authorization.password):
#                 return jsonify({"error": "Unauthorized"}), 401
#             if user.role != role:
#                 return jsonify({"error": "Forbidden"}), 403
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator