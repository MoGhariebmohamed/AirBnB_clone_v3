#!/usr/bin/python3
"""to index api """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def service_status():
    """created route returns status of RESTful service
    TODO check if this formatting is okay for json response"""
    return jsonify({'status': "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def object_stats():
    """returns the count of object types"""

    classes = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
                                                                }
    jsonify(classes).status_code = 200
    return jsonify(classes)
