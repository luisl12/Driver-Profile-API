# -*- coding: utf-8 -*-
"""
driver_profile_api.presentation.home_blueprint
-------

This module provides the home blueprint routes.
"""

# packages
from flask import Blueprint


# create home blueprint
home_bp = Blueprint('home_bp', __name__)


# define home route
@home_bp.route("/")
def home():
    return "<h1>DRIVER PROFILE API</h1>"
