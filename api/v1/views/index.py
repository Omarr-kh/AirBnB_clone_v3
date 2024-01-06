#!/usr/bin/python3
""" index file """
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status_check():
    """ returns status OK """
    return jsonify({"status": "OK"})
