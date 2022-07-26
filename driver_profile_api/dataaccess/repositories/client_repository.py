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
            model (db.model): Company model
        """
        self.model = model

    def get_client(self, uuid):
        """
        Get client by uuid

        Args:
            uuid (UUID): Client UUID

        Returns:
            Company: Client instance
        """
        return (
            db.session.query(self.model)
            .filter_by(uuid=uuid)
            .first()
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
                driver = Client(uuid=uuid, name=name, fleets=fleet_list)
            else:
                driver = Client(name=name, fleets=fleet_list)
            db.session.add(driver)
            db.session.commit()
        except SQLAlchemyError as err:
            current_app.logger.exception(err)
            db.session.rollback()
            return False
        else:
            return driver

client_rep = ClientRepository(Client)
