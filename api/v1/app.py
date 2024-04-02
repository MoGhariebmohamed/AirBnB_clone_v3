#!/usr/bin/python3
"""api file main flask """

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_appcontext(exc=None):
    """called on teardown of app context of flask
    """
    storage.close()


@app.errorhandler(404)
def errorhandler_404(error):
    """response to 404 json"""
    error_404 = {"error": "Not found"}
    return jsonify(error_404), 404


if __name__ == "__main__":
    """required to run flask"""

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    fetched_host = os.environ.get('HBNB_API_HOST')
    fetched_port = os.environ.get('HBNB_API_PORT')
    if fetched_host is None:
        fetched_host = '0.0.0.0'
    if fetched_port is None:
        fetched_port = 5000
    app.run(debug=True, host=fetched_host, port=fetched_port, threaded=True)
