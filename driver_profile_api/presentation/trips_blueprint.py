# -*- coding: utf-8 -*-
"""
driver_profile_api.presentation.trips_blueprint
-------

This module provides the trips blueprint routes.
"""

# packages
from flask import (
    Blueprint,
    request as req,
    current_app
)
import uuid
# utils
from ..utils.utils import (
    InvalidAPIUsage,
    validade_media_type
)
# repositories
from ..dataaccess.repositories.trip_repository import trip_rep
from ..dataaccess.repositories.company_repository import company_rep
from ..dataaccess.repositories.driver_repository import driver_rep 


# create trips blueprint
trips_bp = Blueprint('trips_bp', __name__)


# define trips route
@trips_bp.route("/trips", methods=['POST'])
@validade_media_type('application/json')
def trips():

    # get parameters
    try:
        data = req.json
        trip = data['uuid']
        driver = data['driver']
    except Exception:
        current_app.logger.info("Create trip - Invalid parameters.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # verify if uuid's are in UUID format
    try:
        if trip:
            trip_uuid = uuid.UUID(trip)
        driver_uuid = uuid.UUID(driver)
    except ValueError:
        current_app.logger.info("Create trip - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # get driver
    driver = driver_rep.get_driver(uuid=driver_uuid)
    if not driver:
        current_app.logger.info("Create trip - Driver not found.")
        raise InvalidAPIUsage("Driver Not Found.", status_code=404)

    # create trip
    if trip:
        created = trip_rep.create_trip(driver=driver, trip=trip_uuid)
    else:
        created = trip_rep.create_trip(driver=driver)
    if not created:
        current_app.logger.info("Create trip - Unable to create trip.")
        raise InvalidAPIUsage("Unable to create trip.", status_code=500)
        
    # return 200 OK
    return '', 200
