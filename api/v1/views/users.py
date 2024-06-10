#!/usr/bin/python3
"""
This module provides RESTful API endpoints for managing `User` objects
It includes routes to create, retrieve, update, and delete users
"""
from api.v1.views import app_views
from flask import request, abort, jsonify
from models import storage
from models.user import User
from werkzeug.exceptions import BadRequest


@app_views.get("/users", strict_slashes=False)
@app_views.post("/users", strict_slashes=False)
def users():
    """
    Endpoint to manage users

    Methods:
        GET: Retrieves all users
        POST: Creates a new user and returns it with
        201 created status code.

    Returns:
        Response: JSON response with users data or success/error message.
    """
    if request.method == "GET":
        all_users = storage.all(User).values()
        list_users = []
        for user in all_users:
            list_users.append(user.to_dict())
        return jsonify(list_users)
    elif request.method == "POST":
        try:
            req_data = request.get_json()
        except BadRequest:
            abort(400, description="Not a JSON")
        if not req_data:
            abort(400, description="Not a JSON")

        required_fields = ["email", "password"]
        for field in required_fields:
            if field not in req_data:
                abort(400, description=f"Missing {field}")
        new_user = User(**req_data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.get("/users/<user_id>", strict_slashes=False)
@app_views.put("/users/<user_id>", strict_slashes=False)
@app_views.delete("/users/<user_id>", strict_slashes=False)
def user_objs(user_id):
    """
    Endpoint to manage individual user objects.

    Methods:
        GET: Retrieves a user with a specific ID.
        PUT: Updates a specific a user by ID.
        DELETE: Deletes a specific user by ID.

    Args:
        user_id (str): The ID of the user to be managed.

    Returns:
        Response: JSON response with user data or success/error message.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return ({}), 200
    elif request.method == "PUT":
        try:
            req_data = request.get_json()
        except BadRequest:
            abort(400, description="Not a JSON")
        if not req_data:
            abort(400, description="Not a JSON")
        for k, v in req_data.items():
            if k not in ["id", "email", "updated_at", "created_at"]:
                setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
