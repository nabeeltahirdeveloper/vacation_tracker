#!/usr/bin/python3
"""Index Lunching app script"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
  """stats of all objects route :return json of all objs"""
  data = {
    "users": storage.count("User"),
    "employments": storage.count("Employment"),
    "vacation_requests": storage.count("Request"),
    "units": storage.count("Unit")
  }
  res = jsonify(data)
  res.status_code = 200
  
  return res
  
  
  
