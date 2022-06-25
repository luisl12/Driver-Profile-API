# -*- coding: utf-8 -*-
"""
driver_profile_api.utils.utils
-----------------

This module provides utilities for the API.
"""

# packages
from flask import request as req
from functools import wraps


def validade_media_type(mtype):
    """
    Validate request media type

    Args:
        mtype (str): Media type
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if req.content_type is None:
                raise InvalidAPIUsage("Unsupported Media Type.", status_code=415)
            target = req.content_type.split(';')[0]
            if target != mtype:
                raise InvalidAPIUsage("Unsupported Media Type.", status_code=415)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class InvalidAPIUsage(Exception):
    """
    Custom HTTP error class
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
