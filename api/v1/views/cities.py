#!/usr/bin/python3
"""
This module provides RESTful API endpoints for managing `City` objects
within the context of their associated `State`. It includes routes to
create, retrieve, update, and delete cities, as well as retrieve all cities
in a specific state.
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest


@app_views.get("/states/<state_id>/cities", strict_slashes=False)
@app_views.post("/states/<state_id>/cities", strict_slashes=False)
def state_cities(state_id):
    """
    Endpoint to manage cities related to a specific state.

    Methods:
        GET: Retrieves all cities linked to the specified state.
        POST: Creates a new city linked to the specified state.

    Args:
        state_id (str): The ID of the state whose cities are being managed.

    Returns:
        Response: JSON response with cities data or success/error message.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        cities = storage.all(City).values()
        st_ctz = [c.to_dict() for c in cities if c.state_id == state_id]
        return jsonify(st_ctz)
    elif request.method == "POST":
        try:
            req_data = request.get_json()
            if not req_data:
                abort(400, description="Not a JSON")
            if "name" not in req_data:
                abort(400, description="Missing name")
            new_city = City(**req_data)
            new_city.state_id = state_id
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201
        except BadRequest:
            abort(400, description="Not a JSON")


@app_views.get("/cities/<city_id>", strict_slashes=False)
@app_views.put("/cities/<city_id>", strict_slashes=False)
@app_views.delete("/cities/<city_id>", strict_slashes=False)
def cities(city_id):
    """
    Endpoint to manage individual city objects.

    Methods:
        GET: Retrieves all cities or a specific city by ID.
        PUT: Updates a specific city by ID.
        DELETE: Deletes a specific city by ID.

    Args:
        city_id (str): The ID of the city to be managed.

    Returns:
        Response: JSON response with cities data or success/error message.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return ({}), 200
    elif request.method == "PUT":
        try:
            req_data = request.get_json()
            if not req_data:
                abort(400, description="Not a JSON")
            for name, value in req_data.items():
                if name not in ["id", "state_id", "created_at", "updated_at"]:
                    setattr(city, name, value)
            storage.save()
            return jsonify(city.to_dict()), 200
        except BadRequest:
            abort(400, description="Not a JSON")
