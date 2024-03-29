# -*- coding: utf-8 -*-
"""
driver_profile_api.domain.trip_service
-------

This file provides the trip business logic.
"""

# repositories
from ..dataaccess.repositories.trip_repository import trip_rep
# external services
from ..dataaccess.services.idreams_service import idreams_service


class TripService:
    """
    Trip Service - Trip business logic
    """

    def create_trip(self, driver, info, profile, uuid=None, fleet=None):
        """
        Create new trip

        Args:
            driver (Driver): Trip driver
            info (dict): Trip info
            profile (str): Trip profile
            uuid (str, optional): Trip UUID. Defaults to None.
            fleet (str, optional): Fleet instance. Defaults to None.

        Returns:
            trip (Trip): Trip created
        """
        t = trip_rep.create_trip(driver=driver, info=info, profile=profile, uuid=uuid, fleet=fleet)
        if not t:
            return None
        trip = {
            'uuid': str(t.uuid),
            'start': str(t.start),
            'end': str(t.end),
            'duration': t.duration,
            'distance': t.distance,
            'profile': t.profile,
            'fleet': t.fleet.uuid if t.fleet else None
        }
        return trip
        
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

    def get_idreams_trip_data(self, trip):
        """
        Get i-DREAMS trip data

        Args:
            trip (str): Trip UUID

        Returns:
            data (dict): Retrieved trip data
        """
        return idreams_service.get_trip_data(trip)



trip_service = TripService()
