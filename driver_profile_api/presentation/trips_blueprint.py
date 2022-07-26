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
from ..utils.ml_model_utils import predict_profile
# services
from ..domain.driver_service import driver_service
from ..domain.trip_service import trip_service 
from ..dataaccess.repositories.company_repository import company_rep
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

    # get trip uuid
    try:
        trip = data['uuid']
    except KeyError:
        trip = None

    # check info format
    if not isinstance(info, dict):
        current_app.logger.info("Create trip - Invalid info format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)
    
    # check info data
    if (not 'start' in info) or \
        (not 'end' in info) or \
        (not 'duration' in info) or \
        (not 'distance' in info):
        current_app.logger.info("Create trip - Invalid info data.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check data format
    try:
        ts_start = datetime.fromisoformat(info['start'])
        _ = ts_start.strftime(current_app.config['DATETIME_FORMAT'])
        ts_end = datetime.fromisoformat(info['end'])
        _ = ts_end.strftime(current_app.config['DATETIME_FORMAT'])
        float(info['duration'])
        float(info['distance'])
    except Exception:
        current_app.logger.info("Create trip - Invalid info data format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # verify if uuid's are in UUID format
    try:
        if trip:
            trip_uuid = shortuuid.decode(trip)
        driver_uuid = p_uuid.UUID(driver)
    except ValueError:
        current_app.logger.info("Create trip - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # get driver
    driver = driver_service.get_driver(uuid=driver_uuid)
    if not driver:
        current_app.logger.info("Create trip - Driver not found.")
        raise InvalidAPIUsage("Driver Not Found.", status_code=404)

    # create trip
    if trip:
        created = trip_service.create_trip(driver=driver, info=info, uuid=trip_uuid)
    else:
        created = trip_service.create_trip(driver=driver, info=info)
    if not created:
        current_app.logger.info("Create trip - Unable to create trip.")
        raise InvalidAPIUsage("Unable to create trip.", status_code=500)
        
    # return 200 OK
    return '', 200


# define classify trips route
@trips_bp.route("/trips", methods=['PUT'])
@validate_media_type('application/json')
def trip_profile():

    # get request data
    try:
        data = req.json
        uuid = data['uuid']
    except Exception:
        current_app.logger.info("Trip profile - Invalid request.")
        raise InvalidAPIUsage("Bad request.", status_code=400)
    
    # verify if uuid (shortuuid) is in UUID format
    try:
        trip_uuid = shortuuid.decode(uuid)
    except ValueError:
        current_app.logger.info("Trip profile - Wrong uuid's format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if data is in request and if its in correct format
    try:
        trip_instance = data['data']
        f_names = dataset_features()
        for f in f_names:
            assert f in trip_instance
    except KeyError:
        current_app.logger.info("Trip profile - No data provided.")
        trip_instance = None
    except AssertionError:
        current_app.logger.info("Trip profile - Data is not in correct format.")
        raise InvalidAPIUsage("Bad request.", status_code=400)

    # check if trip exists
    trip = trip_service.get_trip(trip_uuid)
    if not trip:
        current_app.logger.info("Trip profile - Trip not found.")
        raise InvalidAPIUsage("Trip Not Found.", status_code=404)

    # get trip distance and duration
    distance = trip.distance
    duration = trip.duration

    # if trip data does not exists in request
    if not trip_instance:
        # get I-Dreams trip data
        trips_data = idreams_service.get_trip_data(uuid)
        # create trip like the dataset
        trip_instance = construct_dataset(trips_data['data'], distance, duration)
    else:
        dist_dur = {'distance': distance, 'duration': duration}
        trip_instance = {**dist_dur, **trip_instance}
        trip_instance = pd.DataFrame([trip_instance])
    
    # fill missing values
    trips = fill_missing_values(trips=trip_instance)

    src = os.path.dirname(os.path.abspath(__file__))
    models = os.path.join(src, '../utils/models')
    path_name = os.path.join(models, 'decision_tree_model')
    prediction = predict_profile(path_name=path_name, data=trips)
    print(prediction)

    # update trip profile
    # trip_service.update_trip_profile(trip_uuid, )

    # return response
    return '', 200
