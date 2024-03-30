#!/usr/bin/python3
"""View for place objects"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def view_city_places(city_id):
    """Returns a list containing all Place objects from a particular city"""
    for city in storage.all(City).values():
        if city.id == city_id:
            places = []
            for place in storage.all(Place).values():
                if place.city_id == city_id:
                    places.append(place.to_dict())
            return jsonify(places)
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a new place object"""
    try:
        place_data = request.get_json(silent=True)
        if not place_data:
            raise ValueError("Not a JSON")
    except ValueError as e:
        raise abort(400, description=str(e))
    for city in storage.all(City).values():
        if city.id == city_id:
            if 'user_id' not in place_data:
                raise abort(400, description="Missing user_id")
            for user in storage.all(User).values():
                if user.id == place_data['user_id']:
                    if 'name' not in place_data:
                        raise abort(400, description="Missing name")
                    new_place = Place(city_id=city_id, **place_data)
                    new_place.save()
                    return jsonify(new_place.to_dict()), 201
            abort(404)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def view_place(place_id):
    """Returns the place with id 'place_id'"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT', 'PATCH'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates the place with id 'place_id'"""
    try:
        place_data = request.get_json(silent=True)
        if not place_data:
            raise ValueError("Not a JSON")
    except ValueError as e:
        raise abort(400, description=str(e))
    for place in storage.all(Place).values():
        if place.id == place_id:
            for k, v in place_data.items():
                ignore = ['id', 'created_at', 'city_id', 'user_id']
                if k not in ignore:
                    setattr(place, k, v)
            place.save()
            return jsonify(place.to_dict()), 200
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes the place with id 'place_id'"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def retrieve_places():
    """ retrieves all Place objects depending of
    the JSON in the body of the request."""
    req = request.get_json(silent=True)
    if req is None:
        raise abort(400, description="Not a JSON")

    places_list = []
    for place in storage.all(Place).values():
        if 'states' in req and len(req['states']) > 0:
            for state_id in req['states']:
                city = storage.get(City, place.city_id)
                if city.state_id == state_id:
                    places_list.append(place)
        if 'cities' in req and len(req['cities']) > 0:
            for city_id in req['cities']:
                if city_id == place.city_id and place not in places_list:
                    places_list.append(place)
        if 'states' not in req or len(req['states']) == 0:
            if 'cities' not in req or len(req['cities']) == 0:
                places_list.append(place)

    delete_list = []
    if 'amenities' in req and len(req['amenities']) > 0:
        for place in places_list:
            for amenity_id in req['amenities']:
                amenity = storage.get(Amenity, amenity_id)
                if amenity not in place.amenities:
                    delete_list.append(place)
                    break

    final_list = []
    for place in places_list:
        if place not in delete_list:
            final_list.append(place.to_dict())

    return jsonify(final_list), 200
