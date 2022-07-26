# -*- coding: utf-8 -*-
"""
driver_profile_api.domain.client_service
-------

This file provides the client business logic.
"""

# repositories
from ..dataaccess.repositories.client_repository import client_rep


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


client_service = ClientService()
