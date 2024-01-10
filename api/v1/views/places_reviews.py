#!/usr/bin/python3
""" Handles everything related to reviews """

from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route("/places/<place_id>/reviews", methods=['GET'])
def get_review_by_place(place_id):
    """Retrieves by id"""
    req_place = storage.get("Place", place_id)
    if not req_place:
        abort(404)
    return jsonify([r.to_dict() for r in req_place.reviews])


@app_views.route("/reviews/<review_id>", methods=['GET'])
def get_review_by_id(review_id):
    """
    Reyrieves a review by id
    """
    req_review = storage.get("Review", review_id)
    if not req_review:
        abort(404)
    return jsonify(req_review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Delete a review with the given id
    """
    req_review = storage.get("Review", review_id)
    if not req_review:
        abort(404)
    storage.delete(req_review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_new_review(place_id):
    """
    Create a new review
    """
    req_place = storage.get("Place", place_id)
    if not req_place:
        abort(404)
    res_json = request.get_json()
    if res_json is None:
        abort(400, 'Not a JSON')
    if 'text' not in res_json:
        abort(400, 'Missing text')
    if 'user_id' not in res_json:
        abort(400, 'Missing user_id')
    get_u = storage.get("User", res_json['user_id'])
    if not get_u:
        abort(404)
    req_review = Review(**res_json)
    req_review.user_id = res_json['user_id']
    req_review.place_id = place_id
    req_review.save()
    return jsonify(req_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """
    Update an review with the given id
    """
    req_review = storage.get("Review", review_id)
    if not req_review:
        abort(404)
    res_json = request.get_json()
    if res_json is None:
        abort(400, 'Not a JSON')
    if 'text' in res_json:
        req_review.text = res_json['text']
    if 'place_id' in res_json:
        req_place = storage.get("Place", res_json['place_id'])
        if not req_place:
            abort(404)
        req_review.place_id = res_json['place_id']
    if 'user_id' in res_json:
        get_u = storage.get("User", res_json['user_id'])
        if not get_u:
            abort(404)
        req_review.user_id = res_json['user_id']
    req_review.save()
    return jsonify(req_review.to_dict()), 200
