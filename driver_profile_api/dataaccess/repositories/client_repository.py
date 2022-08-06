# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.repositories.client_repository
-------

This module provides the client repository.
"""

# packages
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
# models
from ..models.client import Client
from ..models.fleet import Fleet
from driver_profile_api import db


class ClientRepository:
    """
    Client Repository
    """

    def __init__(self, model):
        """
        Client repository constructor

        Args:
            model (db.model): Client model

        """
        self.model = model

    def get_client(self, uuid):
        """
        Get client by uuid

        Args:
            uuid (UUID): Client UUID

        Returns:
            Client: Client instance
        """
        return (
            db.session.query(self.model)
            .filter_by(uuid=uuid)
            .first()
        )

    def get_clients(self):
        """
        Get clients

        Returns:
            List: Clients list
        """
        return (
            db.session.query(self.model).all()
        )

    def create_client(self, name, uuid=None, fleets=[]):
        """
        Create new client

        Args:
            name (str): client name
            uuid (str, optional): Client UUID. Defaults to None.
            fleets (list, optional): Client fleet names. Defaults to None.

        Returns:
            client (Client): Client created
        """
        try:
            fleet_list = []
            if len(fleets) > 0:
                for f in fleets:
                    fleet = Fleet(name=f)
                    db.session.add(fleet)
                    fleet_list.append(fleet)
            if uuid:
                client = Client(uuid=uuid, name=name, fleets=fleet_list)
            else:
                client = Client(name=name, fleets=fleet_list)
            db.session.add(client)
            db.session.commit()
        except SQLAlchemyError as err:
            current_app.logger.exception(err)
            db.session.rollback()
            return False
        else:
            return client

    def update_client_drivers(self, client, drivers):
        """
        Update client drivers

        Args:
            client (Client): Client to be updated
            drivers (list): List of drivers

        Returns:
            bool: True if drivers were updated
        """
        try:
            client.drivers += drivers
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False
        else:
            return True

    def update_client_fleets(self, client, fleets):
        """
        Update client fleets

        Args:
            client (Client): Client to be updated
            fleets (list): Fleets name list

        Returns:
            bool: True if fleets were updated
        """
        fleet_list = []
        if len(fleets) > 0:
            for f in fleets:
                fleet = Fleet(name=f)
                db.session.add(fleet)
                fleet_list.append(fleet)
        try:
            client.fleets += fleet_list
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return False
        else:
            return True

    def get_fleet_trips(self, client_uuid, fleet_uuid):
        """
        Get fleet trips

        Args:
            client_uuid (str): Client UUID
            fleet_uuid (str): Fleet UUID

        Returns:
            str: List of Trips
        """
        fleet = db.session.query(Fleet) \
            .join(self.model) \
            .filter(self.model.uuid==client_uuid) \
            .filter(Fleet.uuid==fleet_uuid).first()
        return fleet
        


client_rep = ClientRepository(Client)
