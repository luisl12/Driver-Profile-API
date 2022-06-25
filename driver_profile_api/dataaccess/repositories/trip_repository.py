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

    def create_trip(self, driver, uuid=None):
        """
        Create new trip

        Args:
            driver (Driver): Trip driver
            uuid (str, optional): Trip UUID. Defaults to None.

        Returns:
            trip (Trip): Trip created
        """
        try:
            if uuid:
                trip = Trip(uuid=uuid, driver=driver)
            else:
                trip = Trip(driver=driver)
            db.session.add(trip)
            db.session.commit()
        except SQLAlchemyError as err:
            current_app.logger.exception(err)
            db.session.rollback()
            return False
        else:
            return trip

trip_rep = TripRepository(Trip)
