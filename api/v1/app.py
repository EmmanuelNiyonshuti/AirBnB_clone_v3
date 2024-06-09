#!/usr/bin/python3
"""
This module initializes and runs the Flask web application
for the AirBnB clone project.
It sets up the Flask app instance, registers the blueprint for routing,
and defines a teardown function to close the storage session
after each request.
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

"""Create an instance of the Flask class for the web application"""
app = Flask(__name__)
"""
Register the blueprint with the Flask app instance
This blueprint contains the route definitions for the API endpoints
"""
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    This function is called when the app context tears down.
    It ensures the storage session is closed after each request.
    """
    storage.close()


"""Run the Flask web server"""
if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
