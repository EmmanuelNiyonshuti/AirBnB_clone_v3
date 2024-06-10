#!/usr/bin/python3
"""
This module provides RESTful API endpoints for managing `Amenity` objects
 It includes routes to create, retrieve, update, and delete amenities
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.get("/amenities", strict_slashes=False)
@app_views.post("/amenities", strict_slashes=False)
def amenities():
    """
    Endpoint to manage amenities

    Methods:
        GET: Retrieves all amenities
        POST: Creates a new amenity and returns it with
        201 created status code.

    Returns:
        Response: JSON response with amenities data or success/error message.
    """
    amenities = storage.all(Amenity).values()
    if request.method == "GET":
        amenities_list = []
        for amenity in amenities:
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)
    elif request.method == "POST":
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        if "name" not in req_data.keys():
            abort(400, "Missing name")
        new_amenity = Amenity(**req_data)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.get("/amenities/<amenity_id>", strict_slashes=False)
@app_views.delete("/amenities/<amenity_id>", strict_slashes=False)
@app_views.put("/amenities/<amenity_id>", strict_slashes=False)
def amenity_obj(amenity_id):
    """
    Endpoint to manage individual emenity objects.

    Methods:
        GET: Retrieves amenity with a specific ID.
        PUT: Updates a specific amenity by ID.
        DELETE: Deletes a specific amenity by ID.

    Args:
        amenity_id (str): The ID of the amenity to be managed.

    Returns:
        Response: JSON response with amenity data or success/error message.
    """
    amenity = storage.get(Amenity, amenity_id)
    if request.method == "GET":
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    elif request.method == "DELETE":
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return ({}), 200
    elif request.method == "PUT":
        if amenity is None:
            abort(404)
        req_data = request.get_json()
        if not req_data:
            abort(400, "Not a JSON")
        for k, v in req_data.items():
            if k not in ["id", "created_at", "updated_at"]:
                setattr(amenity, k, v)
        storage.save()
        return (amenity.to_dict()), 200
