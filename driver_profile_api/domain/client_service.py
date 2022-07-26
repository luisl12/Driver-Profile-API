# -*- coding: utf-8 -*-
"""
driver_profile_api.domain.client_service
-------

This file provides the client business logic.
"""

# repositories
from ..dataaccess.repositories.client_repository import client_rep
from ..dataaccess.repositories.fleet_repository import fleet_rep
from ..dataaccess.repositories.driver_repository import driver_rep


class ClientService:
    """
    Client Service - Client business logic
    """

    def create_client(self, name, uuid=None, fleets=[]):
        """
        Create new client

        Args:
            name (str): client name
            uuid (str, optional): Driver UUID. Defaults to None.
            fleets (list, optional): Client fleet names. Defaults to None.

        Returns:
            client (Client): Client created
        """
        return client_rep.create_client(name, uuid, fleets)

    def get_client(self, uuid):
        """
        Get client

        Args:
            uuid (str): Client UUID

        Returns:
            client (Client): Client
        """
        return client_rep.get_client(uuid)

    def get_fleet(self, uuid):
        """
        Get fleet

        Args:
            uuid (str): Fleet UUID

        Returns:
            fleet (Fleet): Fleet
        """
        return fleet_rep.get_fleet(uuid)

    def update_client_drivers(self, client, drivers):
        """
        Update client drivers

        Args:
            client (Client): Client instance
            drivers (list): List of drivers uuid's
        """
        drivers_list = [driver_rep.get_driver(d) for d in drivers]
        return client_rep.update_client_drivers(client, drivers_list)

    def get_client_fleet_trips(self, client_uuid, fleet_uuid):
        """
        Get client fleet trips

        Args:
            client_uuid (str): Client UUID
            fleet_uuid (str): Fleet UUID

        Returns:
            list: List of Trips info
        """
        trips = client_rep.get_fleet_trips(client_uuid, fleet_uuid)
        trips = [{
            'uuid': str(t.uuid),
            'start': str(t.start),
            'end': str(t.end),
            'duration': t.duration,
            'distance': t.distance,
            'profile': t.profile
        } for t in trips]
        return trips

    def update_client_fleets(self, client, fleets):
        """
        Update client fleets

        Args:
            client (Client): Client to be updated
            fleets (list): Fleets name list

        Returns:
            bool: True if fleets were updated
        """
        names = [f.name for f in client.fleets]
        in_common = list(set(names) & set(fleets))
        for f in in_common:
            fleets.remove(f)
        return client_rep.update_client_fleets(client, fleets)


client_service = ClientService()
