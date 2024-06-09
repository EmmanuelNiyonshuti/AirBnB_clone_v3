#!/usr/bin/python3
"""
This module defines the routes for managing State objects in the REST API.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest


@app_views.route("/states", methods=["GET", "POST"], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def states(state_id=None):
    """
    Retrieves a list of all State objects or handles
    CRUD operations for a single State object.

    For GET method:
        - If state_id is None, retrieves a list of all State objects.
        - If state_id is provided, retrieves the State object
        with the given ID.

    For POST method:
        - Creates a new State object with the provided JSON data
        in the request body.
        - Returns the newly created State object as a JSON response.

    For PUT method:
        - Updates an existing State object with the provided JSON data
        in the request body.
        - Returns the updated State object as a JSON response.

    For DELETE method:
        - Deletes the State object with the provided ID.
        - Returns an empty JSON response with status code 200
        upon successful deletion.

    Parameters:
        state_id (str): The ID of the State object to be retrieved,
        updated, or deleted.

    Returns:
        json: JSON response containing State object(s) or status message.
    """

    if state_id is None:
        if request.method == "GET":
            states = storage.all(State).values()
            state_list = [state.to_dict() for state in states]
            return jsonify(state_list)
        elif request.method == "POST":
            try:
                data = request.get_json()
            except BadRequest:
                return jsonify(description="Not a JSON"), 400
            if "name" not in data.keys():
                return jsonify(description="Missing Name"), 400
            new_state = State(**data)
            storage.new(new_state)
            storage.save()
            return jsonify(new_state.to_dict()), 201
    else:
        try:
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
        except:
            abort(404)
        if request.method == "GET":
            return jsonify(state.to_dict())

        elif request.method == "DELETE":
            storage.delete(state)
            storage.save()
            return jsonify({}), 200

        elif request.method == "PUT":
            try:
                data = request.get_json()
            except BadRequest:
                return jsonify(description="Not a JSON"), 400

            data = request.get_json()
            for k, v in data.items():
                if k not in storage.all(State).values():
                    setattr(state, k, v)
            storage.save()
            return jsonify(state.to_dict()), 200
