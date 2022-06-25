# -*- coding: utf-8 -*-
"""
driver_profile_api.presentation.errors_blueprint
-------

This module provides the errors blueprint handlers.
"""

# packages
from flask import Blueprint, jsonify
# utils
from ..utils.utils import InvalidAPIUsage


# create errors blueprint
errors_bp = Blueprint('errors_bp', __name__)


# define error handler for all of the application
@errors_bp.app_errorhandler(InvalidAPIUsage)
def handle_error_invalid_api(error):
    response = {
        'title': 'Error ' + str(error.status_code),
        'message': error.message
    }
    return jsonify(response), error.status_code


# deal with HTTP 405 error - Invalid HTTP method
@errors_bp.app_errorhandler(405)
def handle_error_405(error):
    response = {
        'title': error.name,
        'message': error.description
    }
    return jsonify(response), error.code


# deal with HTTP 404 error - Not found
@errors_bp.app_errorhandler(404)
def handle_error_404(error):
    response = {
        'title': error.name,
        'message': error.description
    }
    return jsonify(response), error.code


# deal with HTTP 413 error - Request too large
@errors_bp.app_errorhandler(413)
def handle_error_413(error):
    response = {
        'title': error.name,
        'message': error.description
    }
    return jsonify(response), error.code
