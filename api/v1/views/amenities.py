#!/usr/bin/python3

"""
Module for handling HTTP requests related to Amenity objects
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, make_amen_jsonponse, request


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_all_amen():
    """
    Retrieve all amenities
    """
    all_amen = storage.all(Amenity)
    amen_json = []
    for amenity in all_amen.values():
        amen_json.append(amenity.to_dict())
    return jsonify(amen_json)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieve an amenity by id
    """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    return jsonify(amen.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Delete an amenity by id
    """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    storage.delete(amen)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """
    Create a new amenity
    """
    amen_json = request.get_json()
    if amen_json is None:
        abort(400, 'Not a JSON')
    if 'name' not in amen_json:
        abort(400, 'Missing name')
    amen = Amenity(**amen_json)
    amen.save()
    return jsonify(amen.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """
    Update an amenity by id
    """
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        abort(404)
    amen_json = request.get_json()
    if amen_json is None:
        abort(400, 'Not a JSON')
    for idx, idy in amen_json.items():
        setattr(amen, idx, idy)
    amen.save()
    return jsonify(amen.to_dict())
