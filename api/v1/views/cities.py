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


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"], strict_slashes=False)
def state_cities(state_id=None):
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
    if state_id:
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
            except BadRequest:
                return jsonify(description="Not a JSON"), 400
            if "name" not in req_data.keys():
                return jsonify(description="Missing Name"), 400
            new_city = City(**req_data)
            new_city.state_id = state_id
            storage.new(new_city)
            storage.save()
            return jsonify(new_city.to_dict()), 201

@app_views.route("/cities", methods=["GET"], strict_slashes=False)
@app_views.route("/cities/<city_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def cities(city_id=None):
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
    if not city_id:
        city_objs = storage.all(City).values()
        cities = [city.to_dict() for city in city_objs]
        return jsonify(cities)
    else:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if request.method == "GET":
            return jsonify(city.to_dict())
        elif request.method == "DELETE":
            storage.delete(city)
            storage.save()
            return jsonify({}), 200
        elif request.method == "PUT":
            try:
                req_data = request.get_json()
                for name, value in req_data.items():
                    if name not in ["id", "state_id", "created_at", "updated_at"]:
                        setattr(city, name, value)
                storage.save()
                return jsonify(city.to_dict()), 200
            except BadRequest:
                return jsonify(description="Not a JSON"), 400
