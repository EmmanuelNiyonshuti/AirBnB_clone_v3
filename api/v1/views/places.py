#!/usr/bin/python3
"""
This module provides RESTful API endpoints for managing `Place` objects
It includes routes to create, retrieve, update, and delete places
"""

from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from flask import request, abort, jsonify
from werkzeug.exceptions import BadRequest


@app_views.get("/cities/<city_id>/places", strict_slashes=False)
@app_views.post("/cities/<city_id>/places", strict_slashes=False)
def city_places(city_id):
    """
    Endpoint to manage places related to a specific city.

    Methods:
        GET: Retrieves all places associated with a specific city.
        POST: Creates a new place in a specific city.

    Args:
        city_id (str): The ID of the city to manage places for.

    Returns:
        Response: JSON response with places data or success/error message.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        places = storage.all(Place).values()
        p = [place.to_dict() for place in places if place.city_id == city.id]
        return jsonify(p)
    elif request.method == "POST":
        try:
            req_data = request.get_json()
        except BadRequest:
            abort(400, description="Not a JSON")
        if not req_data:
            abort(400, description="Not a JSON")
        for k, v in req_data.items():
            if k == "user_id":
                user_id = v
        if storage.get(User, user_id) is None:
            abort(404)
        req_fields = ["user_id", "name"]
        for field in req_fields:
            if field not in req_data:
                abort(400, f"Missing {field}")
        new_place = Place(**req_data)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201


@app_views.get("/places/<place_id>", strict_slashes=False)
@app_views.delete("/places/<place_id>", strict_slashes=False)
@app_views.put("/places/<place_id>", strict_slashes=False)
def place_obj(place_id):
    """
    Endpoint to manage individual place objects.

    Methods:
        GET: Retrieves a place with a specific ID.
        PUT: Updates a specific place by ID.
        DELETE: Deletes a specific place by ID.

    Args:
        place_id (str): The ID of the place to be managed.

    Returns:
        Response: JSON response with place data or success/error message.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    elif request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return ({}), 200
    elif request.method == "PUT":
        try:
            req_data = request.get_json()
        except BadRequest:
            abort(400, description="Not a JSON")
        if not req_data:
            abort(400, description="Not a JSON")
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for k, v in req_data.items():
            if k not in ignore_keys:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
