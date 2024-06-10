#!/usr/bin/python3
"""
This module sets up the blueprint for the views in the AirBnB clone API.
The blueprint allows for the modular organization of routes.
"""
from flask import Blueprint

"""Create an instance of the Blueprint class"""
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

"""Import all the routes """
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
