#!/usr/bin/python3
"""
Module for handling HTTP requests related to User objects
"""

import json
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieve all users
    """
    all_users = storage.all(User).values()
    result = []
    for user in all_users:
        result.append(user.to_dict())
    return jsonify(result)


@app_views.route("/users/<string:user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieve an user by id
    """
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    return jsonify(result.to_dict())


@app_views.route("/users/<string:user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """
    Delete an user by id
    """
    result = storage.get(User, user_id)
    if result is None:
        abort(404)
    storage.delete(result)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def create_new_user():
    """
    Create a new user
    """
    if not request.is_json:
        abort(400, description="Not a JSON")
    result = request.get_json()

    if "password" not in result:
        abort(400, description="Missing password")
    if "email" not in result:
        abort(400, description="Missing email")

    new_user = User(**result)
    storage.new(new_user)
    storage.save()
    return new_user.to_dict(), 201


@app_views.route("/users/<user_id>", methods=['PUT', 'GET'],
                 strict_slashes=False)
def update_user_by_id(user_id):
    """
    Update an user by id
    """
    result = storage.get(User, user_id)
    if not result:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")

    json_file = request.get_json()
    for x, y in json_file.items():
        if x != "id" and x != "updated_at" and x != "created_at":
            setattr(result, x, y)
    storage.save()
    return result.to_dict(), 200
