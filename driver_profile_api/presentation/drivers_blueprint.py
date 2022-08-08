# -*- coding: utf-8 -*-
"""
driver_profile_api.presentation.drivers_blueprint
-------

This module provides the drivers blueprint routes.
"""

# packages
from flask import (
    Blueprint,
    request as req,
    jsonify,
    current_app
)
import uuid as p_uuid
import shortuuid
# utils
from ..utils.utils import (
    InvalidAPIUsage,
    validate_media_type
)
# services
from ..domain.driver_service import driver_service 


# create drivers blueprint
drivers_bp = Blueprint('drivers_bp', __name__)


# define drivers route
@drivers_bp.route("/drivers", methods=['POST'])
@validate_media_type('application/json')
def drivers():

    # get parameters
    try:
        data = req.json
        name = data['name']
        assert isinstance(name, str)
    except Exception:
        current_app.logger.info("Create driver - Invalid request.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if uuid is in request and if its in correct format
    try:
        uuid = data['uuid']
        try:
            driver_uuid = shortuuid.decode(uuid, legacy=True)
        except ValueError:
            driver_uuid = shortuuid.decode(uuid)
    except KeyError:
        current_app.logger.info("Create driver - No uuid provided.")
        driver_uuid = None
    except ValueError:
        current_app.logger.info("Create driver - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # create driver
    if driver_uuid:
        created = driver_service.create_driver(uuid=driver_uuid, name=name)
    else:
        created = driver_service.create_driver(name=name)
    if not created:
        current_app.logger.info("Create driver - Unable to create driver.")
        raise InvalidAPIUsage("Unable to create driver.", status_code=500)
    
    # create response
    resp = jsonify(created)

    # return 200 OK
    return resp


# define get driver trips route
@drivers_bp.route("/drivers/<uuid>/trips", methods=['GET'])
def driver_trips(uuid):
    
    # verify if uuid is in UUID format
    try:
        driver_uuid = p_uuid.UUID(uuid)
    except ValueError:
        current_app.logger.info("Get driver trips - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if driver exists
    driver = driver_service.get_driver(driver_uuid)
    if not driver:
        current_app.logger.info("Get driver trips - Driver not found.")
        raise InvalidAPIUsage("Driver Not Found.", status_code=404)

    # get trips
    trips = driver_service.get_driver_trips(uuid=driver_uuid)
    resp = jsonify(trips)

    # return response
    return resp


# define get driver trips route
@drivers_bp.route("/drivers", methods=['GET'])
def get_drivers():
    
    # get drivers
    drivers = driver_service.get_drivers()

    # create response
    resp = jsonify(drivers)

    # return response
    return resp


# define get driver profile route
@drivers_bp.route("/drivers/<uuid>/profile", methods=['GET'])
def get_driver_profile(uuid):
    
    # verify if uuid is in UUID format
    try:
        driver_uuid = p_uuid.UUID(uuid)
    except ValueError:
        current_app.logger.info("Get driver profile - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if driver exists
    driver = driver_service.get_driver(driver_uuid)
    if not driver:
        current_app.logger.info("Get driver profile - Driver not found.")
        raise InvalidAPIUsage("Driver Not Found.", status_code=404)

    # calculate driver profile
    driver = driver_service.get_driver_profile(driver_uuid)
    if not driver:
        current_app.logger.info("Get driver profile - Driver must have at least 2 trips.")
        raise InvalidAPIUsage("Driver must have at least 2 trips.", status_code=400)

    # create response
    resp = jsonify(driver)

    # return response
    return resp