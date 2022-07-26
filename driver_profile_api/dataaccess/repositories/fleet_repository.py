# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.repositories.fleet_repository
-------

This module provides the fleet repository.
"""

# packages
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
# models
from ..models.fleet import Fleet
from driver_profile_api import db


class FleetRepository:
    """
    Fleet Repository
    """

    def __init__(self, model):
        """
        Fleet repository constructor

        Args:
            model (db.model): Fleet model
        """
        self.model = model

    def get_fleet(self, uuid):
        """
        Get fleet by uuid

        Args:
            uuid (UUID): Fleet UUID

        Returns:
            fleet: Fleet instance
        """
        return (
            db.session.query(self.model)
            .filter_by(uuid=uuid)
            .first()
        )
        


fleet_rep = FleetRepository(Fleet)
