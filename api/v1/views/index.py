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
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models.amenity import Amenity

    obj_dict = {}
    objs = {"amenities": Amenity, "cities": City,
            "places": Place, "reviews": Review, "states": State, "users": User}
    for k, v in objs.items():
        obj_dict[k] = storage.count(v)
    return jsonify(obj_dict)
