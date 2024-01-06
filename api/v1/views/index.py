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
        "amenities": storage.count("Amenities"),
        "cities": storage.count("Cities"),
        "places": storage.count("Places"),
        "reviews": storage.count("Reviews"),
        "states": storage.count("States"),
        "users": storage.count("Users")
    })
