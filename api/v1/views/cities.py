#!/usr/bin/python3

"""
Module for handling HTTP requests related to City objects
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state_id(state_id):
    """
    Retrieve all cities by state id
    """
    req_state = storage.get(State, state_id)
    if req_state is None:
        abort(404, "State not found")
    cities_list = [city.to_dict() for city in req_state.cities]
    return jsonify(cities_list)


@app_views.route("/cities/<string:city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieve a city by id
    """
    req_city = storage.get(City, city_id)
    if req_city is None:
        abort(404, "City not found")
    return jsonify(req_city.to_dict())


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """
    Delete a city by id
    """
    req_city = storage.get(City, city_id)
    if req_city is None:
        abort(404, "City not found")
    storage.delete(req_city)
    return jsonify({}), 200


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_city_with_state_id(state_id):
    """
    Create a city by state id
    """
    req_state = storage.get(State, state_id)
    if req_state is None:
        abort(404, "State not found")
    city_json = request.get_json()
    if city_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in city_json:
        abort(400, 'Missing "name"')
    new_city = City(**city_json)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city_by_id(city_id):
    """
    Update a city by id
    """
    req_city = storage.get(City, city_id)
    if req_city is None:
        abort(404, "City not found")
    city_json = request.get_json()
    if city_json is None:
        abort(400, 'Not a JSON')
    for k, v in city_json.items():
        setattr(req_city, k, v)
    req_city.save()
    return jsonify(req_city.to_dict()), 200
