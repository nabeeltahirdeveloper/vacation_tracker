#!/usr/bin/python3
"""script to generate a flask application server"""

from flask import Flask, jsonify, request, make_response, abort, render_template
from api.v1.views import app_views
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(obj):
    """teardown method"""
    storage.close()
    
@app.errorhandler(404)
def not_found(exception):
    """error handler"""
    return make_response(jsonify({'error': 'Not found'}), 404)
  
if __name__ == "__main__":
  host = getenv("vacation_tracker_API_host", "0.0.0.0")
  port = getenv("vacation_tracker_API_port", 5000)
  app.run(host=host, port=port, threaded=True)
