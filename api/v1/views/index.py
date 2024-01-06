#!/usr/bin/python3
""" index file """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status_check():
    """ returns status OK """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """ returns count of all classes' objects """
    return jsonify({
        "amenities": storage.count("amenities"),
        "cities": storage.count("cities"),
        "places": storage.count("places"),
        "reviews": storage.count("reviews"),
        "states": storage.count("states"),
        "users": storage.count("users")
    })
