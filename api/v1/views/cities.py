#!/usr/bin/python3
"""index file"""
from datetime import datetime
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects of a State with GET request
    create a new city with POST request"""

    state = storage.get(State, state_id)
    if state is None:
        raise abort(404)

    if request.method == 'GET':
        cities_list = state.cities
        cities_to_dict = [city.to_dict() for city in cities_list]
        return jsonify(cities_to_dict), 200

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400
        else:
            try:
                data = request.get_json()
            except BadRequest:
                return jsonify({'error': 'Not a JSON'}), 400

        if 'name' not in data.keys():
            return jsonify({'error': 'Missing name'}), 400

        data.update({'state_id': state_id})
        city = City(**data)
        storage.new(city)
        storage.save()
        return jsonify((city.to_dict())), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """Retrieves the list of all City objects of a State"""
    city = storage.get(City, city_id)
    if city is None:
        raise abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({'error': 'Not a JSON'}), 400

        try:
            data = request.get_json()
        except BadRequest:
            return jsonify({'error': 'Not a JSON'}), 400

        for att in ['id', 'state_id', 'created_at', 'updated_at']:
            if att in data.keys():
                del data[att]

        for key, value in data.items():
            setattr(city, key, value)

        # I've noticed in the example that updated_at attribute get updated.
        setattr(city, 'updated_at', datetime.utcnow())

        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 200
