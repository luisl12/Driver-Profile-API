# -*- coding: utf-8 -*-
"""
driver_profile_api.domain.client_service
-------

This file provides the client business logic.
"""

# packages
from flask import current_app
import numpy as np
import itertools
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
        c = client_rep.create_client(name, uuid, fleets)
        if not c:
            return None
        driver = {
            'uuid': str(c.uuid),
            'name': str(c.name),
            'drivers': [d.uuid for d in c.drivers],
            'fleets': [f.uuid for f in c.fleets]
        }
        return driver

    def get_client(self, uuid):
        """
        Get client

        Args:
            uuid (str): Client UUID

        Returns:
            client (Client): Client
        """
        return client_rep.get_client(uuid)

    def get_clients(self):
        """
        Get clients

        Returns:
            client (Client): Client
        """
        clients = client_rep.get_clients()
        clients = [{
            'uuid': str(c.uuid),
            'name': str(c.name),
            'drivers': [d.uuid for d in c.drivers],
            'fleets': [f.uuid for f in c.fleets]
        } for c in clients]
        return clients

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
        } for t in trips.trips]
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

    def get_fleet_profile(self, client_uuid, fleet_uuid):
        """
        Get fleet profile

        Args:
            client_uuid (str): Client UUID
            fleet_uuid (str): Fleet UUID

        Returns:
            profile (str): Fleet profile
        """
        trips = client_rep.get_fleet_trips(client_uuid, fleet_uuid).trips
        # must have at least 3 trips
        if len(trips) < 3:
            return None
        # get profiles dict
        prof_dict = current_app.config['PROFILES']
        # convert profile str to int
        profiles = [prof_dict[t.profile] for t in trips]
        # calculate gain loss func for all trips
        gain_loss = [np.log(y/x) for x, y in zip(profiles, profiles[1:])]
        # calculate fleet volatility
        fleet_volatility = np.std(gain_loss)
        # get most common profile
        # if 2/3 profiles are most common: choose de most sequently common
        # if there is no most sequently common or there is more than 1: choose most recent
        pfs, counts = np.unique(profiles, return_counts=True)
        highest_count = pfs[counts == counts.max()]
        if len(highest_count) > 1:
            l = [(i[0], len(list(i[1]))) for i in itertools.groupby(profiles)][::-1]
            fleet_profile = max(l, key=lambda x:x[1])[0]
        else:
            fleet_profile = highest_count[0]

        # create behavior message to warn if volatility is high
        if fleet_volatility <= 0.2:
            status = 'Consistent fleet behavior over time.'
        elif fleet_volatility > 0.2 and fleet_volatility <= 0.4:
            status = 'Inconsistent fleet behavior over time.'
        else:
            status = 'Very inconsistent fleet behavior over time.'
        info = {
            'fleet_profile': list(prof_dict.keys())[list(prof_dict.values()).index(fleet_profile)],
            'behavior_status': {
                'status': status,
                'volatility': fleet_volatility
            }
        }
        return info


client_service = ClientService()
