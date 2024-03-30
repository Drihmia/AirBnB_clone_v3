#!/usr/bin/python3
"""View for user objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def view_users():
    """Returns a list containing all User objects"""
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user object"""
    user_data = request.get_json(silent=True)
    if not user_data:
        raise abort(400, description="Not a JSON")
    if 'email' not in request.json:
        raise abort(400, description="Missing email")
    if 'password' not in request.json:
        raise abort(400, description="Missing password")
    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False)
def view_user(user_id):
    """Returns the user with id 'user_id'"""
    for user in storage.all(User).values():
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['PUT', 'PATCH'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates the user with id 'user_id'"""
    user_dict = request.get_json(silent=True)
    if not user_dict:
        raise abort(400, description="Not a JSON")
    for user in storage.all(User).values():
        if user.id == user_id:
            ignore = ['id', 'created_at', 'email', 'updated_at']
            for k, v in user_dict.items():
                if k not in ignore:
                    setattr(user, k, v)
            user.save()
            return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes the user with id 'user_id'"""
    for user in storage.all(User).values():
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
    abort(404)
