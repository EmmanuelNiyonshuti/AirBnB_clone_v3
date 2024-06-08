#!/usr/bin/python3
"""
This module sets up the blueprint for the views in the AirBnB clone API.
The blueprint allows for the modular organization of routes.
"""
from flask import Blueprint

"""Create an instance of the Blueprint class"""
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

"""Import all the routes from the index module"""
from api.v1.views.index import *