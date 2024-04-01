#!/usr/bin/python3
"""to index api """
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', strict_slashes=False)
def service_status():
    """created route returns status of RESTful service
    TODO check if this formatting is okay for json response"""
    return jsonify({'status': 'OK'})
