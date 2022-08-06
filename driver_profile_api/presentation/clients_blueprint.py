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

from numpy import c_
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
        assert isinstance(uuid, str)
        client_uuid = p_uuid.UUID(uuid)
    except KeyError:
        current_app.logger.info("Create client - No uuid provided.")
        client_uuid = None
    except (ValueError, AssertionError):
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
    
    # create response
    resp = jsonify(created)

    # return 200 OK
    return resp


# define get clients route
@clients_bp.route("/clients", methods=['GET'])
def get_clients():

    # get clients
    clients = client_service.get_clients()

    # create response
    resp = jsonify(clients)

    # return response
    return resp


# define update client drivers route
@clients_bp.route("/clients/<uuid>/drivers", methods=['PATCH'])
@validate_media_type('application/json')
def update_client_drivers(uuid):

    # get parameters
    try:
        data = req.json
        drivers = data['drivers']
    except Exception:
        current_app.logger.info("Update client drivers - Invalid request.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if uuid is in correct format
    try:
        client_uuid = p_uuid.UUID(uuid)
    except ValueError:
        current_app.logger.info("Update client drivers - Wrong uuid format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if uuid's are in correct format
    try:
        assert isinstance(drivers, list) 
        list(map(lambda f: p_uuid.UUID(f), drivers))
    except (ValueError, AttributeError, AssertionError):
        current_app.logger.info("Update client drivers - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # get client
    client = client_service.get_client(client_uuid)
    if not client:
        current_app.logger.info("Update client drivers - Client not found.")
        raise InvalidAPIUsage("Client not found.", status_code=404)

    # update client drivers
    updated = client_service.update_client_drivers(client, drivers)
    if not updated:
        current_app.logger.info("Update client drivers - Unable to update client drivers.")
        raise InvalidAPIUsage("Unable to update client drivers.", status_code=500)
        
    # return 200 OK
    return '', 200


# define add fleet to client route
@clients_bp.route("/clients/<uuid>/fleets", methods=['PATCH'])
@validate_media_type('application/json')
def update_client_fleets(uuid):

    # get parameters
    try:
        data = req.json
        fleets = data['fleets']
        assert isinstance(fleets, list)
        assert all(isinstance(f, str) for f in fleets)
    except (Exception, AssertionError):
        current_app.logger.info("Add client fleet - Invalid request.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if uuid is in correct format
    try:
        client_uuid = p_uuid.UUID(uuid)
    except ValueError:
        current_app.logger.info("Add client fleet - Wrong uuid format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # get client
    client = client_service.get_client(client_uuid)
    if not client:
        current_app.logger.info("Add client fleet - Client not found.")
        raise InvalidAPIUsage("Client not found.", status_code=404)

    # update client drivers
    updated = client_service.update_client_fleets(client, fleets)
    if not updated:
        current_app.logger.info("Add client fleet - Unable to update client fleets.")
        raise InvalidAPIUsage("Unable to update client fleets.", status_code=500)
        
    # return 200 OK
    return '', 200


# define get trips of a client fleet route
@clients_bp.route("/clients/<c_uuid>/fleets/<f_uuid>/trips", methods=['GET'])
def get_fleet_trips(c_uuid, f_uuid):

    # check if uuid's are in correct format
    try:
        client_uuid = p_uuid.UUID(c_uuid)
        fleet_uuid = p_uuid.UUID(f_uuid)
    except ValueError:
        current_app.logger.info("Get fleet trips - Wrong uuid format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # get client
    client = client_service.get_client(client_uuid)
    if not client:
        current_app.logger.info("Get fleet trips - Client not found.")
        raise InvalidAPIUsage("Client not found.", status_code=404)

    # get fleet
    fleet = client_service.get_fleet(fleet_uuid)
    if not fleet:
        current_app.logger.info("Get fleet trips - Fleet not found.")
        raise InvalidAPIUsage("Fleet not found.", status_code=404)

    # get client fleet trips
    trips = client_service.get_client_fleet_trips(client_uuid, fleet_uuid)
    resp = jsonify(trips)
        
    # return 200 OK
    return resp


# define fleet profile route
@clients_bp.route("/clients/<c_uuid>/fleets/<f_uuid>/profile", methods=['GET'])
def get_fleet_profile(c_uuid, f_uuid):

    # check if uuid's are in correct format
    try:
        client_uuid = p_uuid.UUID(c_uuid)
        fleet_uuid = p_uuid.UUID(f_uuid)
    except ValueError:
        current_app.logger.info("Get fleet profile - Wrong uuid format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # get client
    client = client_service.get_client(client_uuid)
    if not client:
        current_app.logger.info("Get fleet trips - Client not found.")
        raise InvalidAPIUsage("Client not found.", status_code=404)

    # get fleet
    fleet = client_service.get_fleet(fleet_uuid)
    if not fleet:
        current_app.logger.info("Get fleet trips - Fleet not found.")
        raise InvalidAPIUsage("Fleet not found.", status_code=404)

    # calculate fleet profile
    fleet = client_service.get_fleet_profile(client_uuid, fleet_uuid)
    if not fleet:
        current_app.logger.info("Get fleet profile - Fleet must have at least 2 trips.")
        raise InvalidAPIUsage("Fleet must have at least 2 trips.", status_code=400)

    # create response
    resp = jsonify(fleet)

    # return response
    return resp
