#!/usr/bin/pytho3
"""
This module defines routes related to the status of the API.
"""

from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status")
def status():
    """
    Returns the status of the API.

    This route responds to a GET request with a JSON object
    indicating that the API is up and running.

    Returns:
        JSON response: A JSON object with a key "status" and value "OK".
    """
    return jsonify({"status": "OK" })
