#!/usr/bin/python3
"""
This module defines routes related to the status of the API.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    """
    Returns the status of the API.

    This route responds to a GET request with a JSON object
    indicating that the API is up and running.

    Returns:
        JSON response: A JSON object with a key "status" and value "OK".
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """
    Retrieves The number of each object by type.
    """
    from models.engine.db_storage import classes

    obj_dict = {}
    for k, v in classes.items():
        obj_dict[k] = storage.count(v)
    return jsonify(obj_dict)
