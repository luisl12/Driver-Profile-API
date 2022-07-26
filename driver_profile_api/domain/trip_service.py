# -*- coding: utf-8 -*-
"""
driver_profile_api.domain.trip_service
-------

This file provides the trip business logic.
"""

# repositories
from ..dataaccess.repositories.trip_repository import trip_rep


class TripService:
    """
    Trip Service - Trip business logic
    """

    def create_trip(self, driver, info, uuid=None):
        """
        Create new trip

        Args:
            driver (Driver): Trip driver
            info (dict): Trip info
            uuid (str, optional): Trip UUID. Defaults to None.

        Returns:
            trip (Trip): Trip created
        """
        return trip_rep.create_trip(driver=driver, info=info, uuid=uuid)

    def get_trip(self, uuid):
        """
        Get trip

        Args:
            uuid (str): Trip UUID

        Returns:
            trip (Trip): Trip
        """
        return trip_rep.get_trip(uuid=uuid)

    def update_trip_profile(self, uuid, new_profile):
        """
        Update trip profile

        Args:
            uuid (str): Trip UUID
            new_profile (str): New trip profile

        Returns:
            updated (bool): True if profile was updated
        """
        trip = self.get_trip(uuid)
        return trip_rep.update_trip_profile(trip, new_profile)



trip_service = TripService()
