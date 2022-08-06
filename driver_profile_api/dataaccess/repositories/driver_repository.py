# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.repositories.driver_repository
-------

This module provides the driver repository.
"""

# packages
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
# models
from ..models.driver import Driver
from driver_profile_api import db


class DriverRepository:
    """
    Driver Repository
    """

    def __init__(self, model):
        """
        Driver repository constructor

        Args:
            model (db.model): Driver model
        """
        self.model = model

    def get_driver(self, uuid):
        """
        Get driver by uuid

        Args:
            uuid (UUID): Driver UUID

        Returns:
            Driver: Driver instance
        """
        return (
            db.session.query(self.model)
            .filter_by(uuid=uuid)
            .first()
        )

    def get_drivers(self):
        """
        Get drivers

        Returns:
            List: Drivers list
        """
        return (
            db.session.query(self.model).all()
        )

    def create_driver(self, name, uuid=None):
        """
        Create new driver

        Args:
            uuid (str, optional): Driver UUID. Defaults to None.
            name (str): Driver name
        Returns:
            driver (Driver): Driver created
        """
        try:
            if uuid:
                driver = Driver(uuid=uuid, name=name)
            else:
                driver = Driver(name=name)
            db.session.add(driver)
            db.session.commit()
        except SQLAlchemyError as err:
            current_app.logger.exception(err)
            db.session.rollback()
            return False
        else:
            return driver

driver_rep = DriverRepository(Driver)
