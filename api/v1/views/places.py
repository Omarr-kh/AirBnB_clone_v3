#!/usr/bin/python3
""" Handles everything related to places """

from models import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/cities/<string:city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieve all places by city id given
    """
    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)
    place_inst = get_city.places
    all_places = []
    for item in place_inst:
        all_places.append(item.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<string:place_id>", methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """
    Reyrieves a place by id
    """
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    return jsonify(place_inst.to_dict())


@app_views.route("/places/<string:place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """
    Delete a place by id
    """
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    storage.delete(place_inst)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_new_place(city_id):
    """
    Create a new place
    """
    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_json:
        abort(400, 'Missing user_id')
    user_data = storage.get("User", req_json['user_id'])
    if user_data is None:
        abort(404)
    if 'name' not in req_json:
        abort(400, 'Missing name')
    req_json['city_id'] = city_id
    place_inst = Place(**req_json)
    place_inst.save()
    return jsonify(place_inst.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """
    Update an place by id
    """
    place_inst = storage.get(Place, place_id)
    if place_inst is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    for idx, idy in req_json.items():
        if idx not in ['id', 'city_id', 'user_id', 'updated_at',
                       'created_at']:
            setattr(place_inst, idx, idy)
    place_inst.save()
    return jsonify(place_inst.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Handles search feature in places
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")

    req_json = request.get_json()

    if req_json and len(req_json):
        req_states = req_json.get('states', None)
        req_cities = req_json.get('cities', None)
        req_amenities = req_json.get('amenities', None)

    if not req_json or not len(req_json) or (
            not req_states and
            not req_cities and
            not req_amenities):
        places = storage.all(Place).values()
        place_arr = [place.to_dict() for place in places]
        return jsonify(place_arr)

    place_arr = []
    if req_states:
        get_s = [storage.get(State, state_id) for state_id in req_states]
        for state in get_s:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            place_arr.append(place)

    if req_cities:
        get_c = [storage.get(City, city_id) for city_id in req_cities]
        for city in get_c:
            if city:
                for place in city.places:
                    if place not in place_arr:
                        place_arr.append(place)

    if req_amenities:
        if not place_arr:
            place_arr = storage.all(Place).values()
        amen = [storage.get(Amenity, amenity_id)
                for amenity_id in req_amenities]
        place_arr = [place for place in place_arr
                     if all([idx in place.amenities
                            for idx in amen])]

    res = []
    for place in place_arr:
        place_dict = place.to_dict()
        place_dict.pop('amenities', None)
        res.append(place_dict)

    return jsonify(res)
