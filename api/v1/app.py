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

if __name__ == "__main__":
    """required to run flask"""

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    fetched_host = os.environ.get('HBNB_API_HOST')
    fetched_port = os.environ.get('HBNB_API_PORT')
    if fetched_host is None:
        fetched_host = '0.0.0.0'
    if fetched_port is None:
        fetched_port = 5000
    app.run(host=fetched_host, port=fetched_port, threaded=True)
