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
    obj_dict = {}
    for obj in storage.all().values():
        class_name = obj.__class__.__name__
        if class_name.endswith('y'):
            key = class_name[:-1].lower() + 'ies'
        else:
            key = class_name.lower() + 's'
        obj_dict[key] = storage.count(class_name)
    return jsonify(obj_dict)
