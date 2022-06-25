# -*- coding: utf-8 -*-
"""
driver_profile_api.domain.driver_service
-------

This file provides the driver business logic.
"""

# repositories
from ..dataaccess.repositories.driver_repository import driver_rep


class DriverService:
    """
    Driver Service - Driver business logic
    """

    def create_driver(self, uuid=None):
        """
        Create new driver

        Args:
            uuid (str, optional): Driver UUID. Defaults to None.

        Returns:
            driver (Driver): Driver created
        """
        return driver_rep.create_driver(uuid)

    def get_driver(self, uuid):
        """
        Create new driver

        Args:
            uuid (str): Driver UUID

        Returns:
            driver (Driver): Driver
        """
        return driver_rep.get_driver(uuid=uuid)

    def get_driver_trips(self, uuid):
        """
        Get driver trips

        Args:
            uuid (str): Driver UUID
        
        Returns:
            trips (dict): Driver trips
        """
        driver = driver_rep.get_driver(uuid=uuid)
        trips = [{
            'uuid': str(t.uuid),
            'start': str(t.start),
            'end': str(t.end),
            'duration': t.duration,
            'distance': t.distance,
            'profile': t.profile
        } for t in driver.trips]
        return trips


driver_service = DriverService()
