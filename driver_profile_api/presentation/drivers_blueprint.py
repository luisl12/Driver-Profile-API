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
    current_app
)
import uuid
# utils
from ..utils.utils import (
    InvalidAPIUsage,
    validade_media_type
)
# repositories
from ..dataaccess.repositories.driver_repository import driver_rep 


# create drivers blueprint
drivers_bp = Blueprint('drivers_bp', __name__)


# define drivers route
@drivers_bp.route("/drivers", methods=['POST'])
@validade_media_type('application/json')
def trips():

    # get parameters
    try:
        data = req.json
        driver = data['driver']
    except Exception:
        current_app.logger.info("Create driver - Invalid parameters.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # verify if uuid is in UUID format
    try:
        if driver:
            driver_uuid = uuid.UUID(driver)
    except ValueError:
        current_app.logger.info("Create driver - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # create driver
    if driver:
        created = driver_rep.create_driver(uuid=driver_uuid)
    else:
        created = driver_rep.create_driver()
    if not created:
        current_app.logger.info("Create driver - Unable to create driver.")
        raise InvalidAPIUsage("Unable to create driver.", status_code=500)
        
    # return 200 OK
    return '', 200
