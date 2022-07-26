# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.repositories.trip_repository
-------

This module provides the trip repository.
"""

# packages
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
# models
from ..models.trip import Trip
from driver_profile_api import db


class TripRepository:
    """
    Trip Repository
    """

    def __init__(self, model):
        """
        Trip repository constructor

        Args:
            model (db.model): Trip model
        """
        self.model = model

    def get_trip(self, uuid):
        """
        Get trip by uuid

        Args:
            uuid (UUID): Trip UUID

        Returns:
            Trip: Trip instance
        """
        return (
            db.session.query(self.model)
            .filter_by(uuid=uuid)
            .first()
        )

    def create_trip(self, driver, info, uuid=None, fleet=None):
        """
        Create new trip

        Args:
            driver (Driver): Trip driver
            info (dict): Trip info
            uuid (str, optional): Trip UUID. Defaults to None.
            fleet (Fleet, optional): Fleet instance. Defaults to None.

        Returns:
            trip (Trip): Trip created
        """
        start = info['start']
        end = info['end']
        duration = info['duration']
        distance = info['distance']
        try:
            if uuid:
                trip = Trip(
                    uuid=uuid, driver=driver, start=start, 
                    end=end, duration=duration, distance=distance,
                    fleet=fleet
                )
            else:
                trip = Trip(
                    driver=driver, start=start, end=end,
                    duration=duration, distance=distance,
                    fleet=fleet
                )
            db.session.add(trip)
            db.session.commit()
        except SQLAlchemyError as err:
            current_app.logger.exception(err)
            db.session.rollback()
            return False
        else:
            return trip

    def update_trip_profile(self, trip, new_profile):
        """
        Update trip profile

        Args:
            trip (Trip): Trip instance
            new_profile (str): New trip profile

        Returns:
            bool: True if profile was updated
        """
        try:
            trip.profile = new_profile
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False
        else:
            return True


trip_rep = TripRepository(Trip)
