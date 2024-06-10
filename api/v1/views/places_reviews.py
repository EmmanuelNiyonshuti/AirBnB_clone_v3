#!/usr/bin/python3
"""
This module provides RESTful API endpoints for managing `User` objects
It includes routes to create, retrieve, update, and delete users
"""
from flask import request, abort, jsonify
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models import storage
from models.user import User

@app_views.get("/places/<place_id>/reviews", strict_slashes=False)
@app_views.post("/places/<place_id>/reviews", strict_slashes=False)
def places_reviews(place_id):
    """
    Handles HTTP requests to retrieve and create reviews for a specific place.

    Methods:
        GET: Retrieves all reviews for a specific place.
        POST: Creates a new review for a specific place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        Response: JSON response containing reviews data or the newly created review.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        reviews = place.reviews
        place_reviews = [rev.to_dict() for rev in reviews]
        return jsonify(place_reviews)
    elif request.method == "POST":
        try:
            req_data = request.get_json()
        except BadRequest:
            abort(400, description="Not a JSON")
        if not req_data:
            abort(400, description="Not a JSON")
        required_keys = ["user_id", "text"]
        for k in required_keys:
            if k not in req_data:
                abort(400, f"Missing {k}") 
        for k, v in req_data.items():
            if k == "user_id":
                user_id = v
        if storage.get(User, user_id) is None:
            abort(404)
        new_review = Review(**req_data)
        new_review.place_id = place_id
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201

@app_views.get("/reviews/<review_id>", strict_slashes=False)
@app_views.delete("/reviews/<review_id>", strict_slashes=False)
@app_views.put("/reviews/<review_id>", strict_slashes=False)
def reviews(review_id):
    """
    Handles HTTP requests to retrieve, delete, or update a specific review.

    Methods:
        GET: Retrieves a specific review by ID.
        DELETE: Deletes a specific review by ID.
        PUT: Updates a specific review by ID.

    Args:
        review_id (str): The ID of the review.

    Returns:
        Response: JSON response containing review data or success/error messages.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return ({}), 200
    elif request.method == "PUT":
        try:
            req_data = request.get_json()
        except BadRequest:
            abort(400, description="Not a JSON")
        if not req_data:
            abort(400, description="Not a JSON")
        keys_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for k, v in req_data.items():
            if k not in keys_ignore:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
    