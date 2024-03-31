#!/usr/bin/python3
"""The main module"""
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources="/*", origins="0.0.0.0")


@app.teardown_appcontext
def tear_down(_=None):
    storage.close()


@app.errorhandler(404)
def page_not_found(_):
    """custom error page with http responde's code of 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(e):
    """custom error page with http responde's code of 400"""
    return make_response(jsonify({'error': "{}".format(
        e.__dict__['description'])}), 400)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    port = int(getenv("HBNB_API_PORT") or 5000)  # to avoid linter warnings.
    app.run(host=host, port=port, threaded=True)
