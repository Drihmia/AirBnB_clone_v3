#!/usr/bin/python3
"""View for state objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def view_states():
    """Returns a list containing all State objects"""
    if request.method == 'GET':
        states = []
        for state in storage.all(State).values():
            states.append(state.to_dict())
        return jsonify(states), 200

    if request.method == 'POST':
        state_data = request.get_json(silent=True)
        if not state_data:
            raise abort(400, description="Not a JSON")
        if 'name' not in state_data:
            raise abort(400, description="Missing name")
        new_state = State(**state_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def update_or_delete_state(state_id):
    """Updates or deletes the state with id 'state_id'"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict()), 200

    if request.method == 'PUT':
        state_dict = request.get_json(silent=True)
        if not state_dict:
            raise abort(400, description="Not a JSON")
        ignore = ['id', 'created_at', 'updated_at']
        for k, v in state_dict.items():
            if k not in ignore:
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
