# -*- coding: utf-8 -*-
"""
driver_profile_api.presentation.trips_blueprint
-------

This module provides the trips blueprint routes.
"""

# packages
import pandas as pd
from flask import (
    Blueprint,
    request as req,
    jsonify,
    current_app
)
import uuid as p_uuid
import shortuuid
from datetime import datetime
import os
# utils
from ..utils.utils import (
    InvalidAPIUsage,
    validate_media_type
)
from ..utils.construct_trip import construct_dataset, dataset_features
from ..utils.missing_values import fill_missing_values
from ..utils.ml_model_utils import predict_trip_profile
# services
from ..domain.driver_service import driver_service
from ..domain.trip_service import trip_service 
from ..domain.client_service import client_service
# external services
from ..dataaccess.services.idreams_service import idreams_service


# create trips blueprint
trips_bp = Blueprint('trips_bp', __name__)


# define trips route
@trips_bp.route("/trips", methods=['POST'])
@validate_media_type('application/json')
def trips():

    # get request data
    try:
        data = req.json
        driver = data['driver']
        info = data['info']
    except Exception:
        current_app.logger.info("Create trip - Invalid request.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # get trip uuid (optional in request - i-DREAMS uuid)
    try:
        trip = data['idreams_uuid']
    except KeyError:
        trip = None

    # check if fleet uuid is in request and if its in correct format
    try:
        fleet = data['fleet']
        assert isinstance(fleet, str)
        fleet_uuid = p_uuid.UUID(fleet)
    except KeyError:
        current_app.logger.info("Create trip - No fleet provided.")
        fleet_uuid = None
    except (ValueError, AssertionError):
        current_app.logger.info("Create trip - Wrong uuid format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check info format
    if not isinstance(info, dict):
        current_app.logger.info("Create trip - Invalid info format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)
        
    try:
        assert 'start' in info
        assert 'end' in info
        assert 'duration' in info
        assert 'distance' in info
    except AssertionError:
        current_app.logger.info("Create trip - Invalid info data.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check data format
    try:
        ts_start = datetime.fromisoformat(info['start'])
        _ = ts_start.strftime(current_app.config['DATETIME_FORMAT'])
        ts_end = datetime.fromisoformat(info['end'])
        _ = ts_end.strftime(current_app.config['DATETIME_FORMAT'])
        duration = float(info['duration'])
        distance = float(info['distance'])
    except Exception:
        current_app.logger.info("Create trip - Invalid info data format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # verify if uuid's are in UUID format
    try:
        if trip:
            assert isinstance(trip, str)
            trip_uuid = shortuuid.decode(trip)
        assert isinstance(driver, str)
        driver_uuid = p_uuid.UUID(driver)
    except (ValueError, AssertionError):
        current_app.logger.info("Create trip - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if data is in request and if its in correct format
    try:
        if not trip:
            trip_instance = data['data']
            f_names = dataset_features()
            for f in f_names:
                assert f in trip_instance
    except KeyError:
        current_app.logger.info("Create trip - No data provided.")
        trip_instance = None
    except AssertionError:
        current_app.logger.info("Create trip - Data is not in correct format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # if trip data does not exists in request
    if trip:
        # get I-Dreams trip data
        trips_data = idreams_service.get_trip_data(trip)
        # create trip like the dataset
        trip_instance = construct_dataset(trips_data['data'], distance, duration)
    else:
        dist_dur = {'distance': distance, 'duration': duration}
        trip_instance = {**dist_dur, **trip_instance}
        trip_instance = pd.DataFrame([trip_instance])

    # get driver
    driver = driver_service.get_driver(uuid=driver_uuid)
    if not driver:
        current_app.logger.info("Create trip - Driver not found.")
        raise InvalidAPIUsage("Driver Not Found.", status_code=404)

    # get fleet
    if fleet_uuid:
        fleet = client_service.get_fleet(fleet_uuid)
        if not fleet:
            current_app.logger.info("Create trip - Fleet not found.")
            raise InvalidAPIUsage("Fleet Not Found.", status_code=404)
    else:
        fleet = None

    # fill trip missing values
    trips = fill_missing_values(trips=trip_instance)
    
    # get ml model
    src = os.path.dirname(os.path.abspath(__file__))
    models = os.path.join(src, '../utils/models')
    model = current_app.config['ML_MODEL_NAME']
    path = os.path.join(models, model)
    prediction = predict_trip_profile(path=path, x_test=trips)

    # update trip profile
    if prediction[0] == 0:
        profile = 'Non-Agressive'
    elif prediction[0] == 1:
        profile = 'Agressive'
    elif prediction[0] == 2:
        profile = 'Risky'

    # create trip
    if trip:
        created = trip_service.create_trip(driver=driver, info=info, profile=profile, uuid=trip_uuid, fleet=fleet)
    else:
        created = trip_service.create_trip(driver=driver, info=info, profile=profile, fleet=fleet)
    if not created:
        current_app.logger.info("Create trip - Unable to create trip.")
        raise InvalidAPIUsage("Unable to create trip.", status_code=500)

    # create response
    resp = jsonify(created)
        
    # return 200 OK
    return resp
