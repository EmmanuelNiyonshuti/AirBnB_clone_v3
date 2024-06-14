#!/usr/bin/python3
"""
Create a new view for the link between Place objects and
Amenity objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage, storage_t


@app_views.get("/places/<place_id>/amenities", strict_slashes=False)
@app_views.delete("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False)
@app_views.post("/places/<place_id>/amenities/<amenity_id>", strict_slashes=False)
def place_amenities(place_id=None, amenity_id=None):
    if storage_t == "db":
        place_obj = storage.get(Place, place_id)
        amenity_obj = storage.get(Amenity, amenity_id)
        if place_obj is None:
            abort(404)
        place_amenities = place_obj.amenities
        if request.method == "GET":
            am_list = [amenity.to_dict() for amenity in place_amenities]
            return jsonify(am_list)
        elif request.method == "DELETE":
            if amenity_obj is None:
                abort(404)
            if amenity_obj not in place_amenities:
                abort(404)
            storage.delete(amenity_obj)
            storage.save()
            return ({}), 200
        elif request.method == "POST":
            if amenity_obj is None:
                abort(404)
            if amenity_obj in place_amenities:
                return jsonify(amenity_obj.to_dict()), 200
            place_amenities.append(amenity_obj)
            storage.save()
            return jsonify(amenity_obj), 201
    else:
        place_obj = storage.get(Place, place_id)
        amenity_obj = storage.get(Amenity, amenity_id)
        place_amenities = place_obj.amenities
        if place_obj is None:
            abort(404)
        if request.method == "GET":
            place_amids = []
        am_list = [amenity.to_dict() for amenity in place_amenities]
        return jsonify(am_list)
        elif request.method == "DELETE":
            if amenity_obj is None:
                abort(404)
            if amenity_obj not in place_amenities:
                abort(404)
            storage.delete(amenity_obj)
            storage.save()
            return ({}), 200
        elif request.method == "POST":
            if amenity_obj is None:
                abort(404)
            if amenity_obj in place_amenities:
                return jsonify(amenity_obj.to_dict()), 200
            place_amenities.append(amenity_obj)
            storage.save()
            return jsonify(amenity_obj), 201
