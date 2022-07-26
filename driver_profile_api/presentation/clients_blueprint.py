# -*- coding: utf-8 -*-
"""
driver_profile_api.presentation.clients_blueprint
-------

This module provides the clients blueprint routes.
"""

# packages
from flask import (
    Blueprint,
    request as req,
    jsonify,
    current_app
)
import uuid as p_uuid
# utils
from ..utils.utils import (
    InvalidAPIUsage,
    validate_media_type
)
# services
from ..domain.client_service import client_service 


# create clients blueprint
clients_bp = Blueprint('clients_bp', __name__)


# define clients route
@clients_bp.route("/clients", methods=['POST'])
@validate_media_type('application/json')
def clients():

    # get parameters
    try:
        data = req.json
        client = data['client']
    except Exception:
        current_app.logger.info("Create client - Invalid request.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if uuid is in request and if its in correct format
    try:
        uuid = data['uuid']
        client_uuid = p_uuid.UUID(uuid)
    except KeyError:
        current_app.logger.info("Create client - No uuid provided.")
        client_uuid = None
    except ValueError:
        current_app.logger.info("Create client - Wrong uuid format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if fleet are in request
    try:
        fleets = data['fleets']
        assert isinstance(fleets, list)
    except (KeyError, AssertionError):
        current_app.logger.info("Create client - No fleets provided.")
        fleets = []

    # create client
    if client_uuid:
        created = client_service.create_client(name=client, uuid=client_uuid, fleets=fleets)
    else:
        created = client_service.create_client(name=client, fleets=fleets)
    if not created:
        current_app.logger.info("Create client - Unable to create client.")
        raise InvalidAPIUsage("Unable to create client.", status_code=500)
        
    # return 200 OK
    return '', 200
