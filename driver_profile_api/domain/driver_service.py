# -*- coding: utf-8 -*-
"""
driver_profile_api.domain.driver_service
-------

This file provides the driver business logic.
"""

# packages
from flask import current_app
import numpy as np
import itertools
# repositories
from ..dataaccess.repositories.driver_repository import driver_rep


class DriverService:
    """
    Driver Service - Driver business logic
    """

    def create_driver(self, name, uuid=None):
        """
        Create new driver

        Args:
            name (str): Driver name
            uuid (str, optional): Driver UUID. Defaults to None.

        Returns:
            driver (Driver): Driver created
        """
        d = driver_rep.create_driver(uuid=uuid, name=name)
        if not d:
            return None
        driver = {
            'uuid': str(d.uuid),
            'name': str(d.name)
        }
        return driver

    def get_driver(self, uuid):
        """
        Get driver

        Args:
            uuid (str): Driver UUID

        Returns:
            driver (Driver): Driver
        """
        return driver_rep.get_driver(uuid=uuid)

    def get_drivers(self):
        """
        Get drivers

        Returns:
            drivers (list): Drivers list
        """
        drivers = driver_rep.get_drivers()
        drivers = [{
            'uuid': str(d.uuid),
            'name': str(d.name),
            'client': d.client.uuid if d.client else None
        } for d in drivers]
        return drivers

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
            'profile': t.profile,
            'fleet': t.fleet.uuid if t.fleet else None
        } for t in driver.trips]
        return trips

    def get_driver_profile(self, uuid):
        """
        Get driver profile

        Args:
            uuid (str): Driver UUID

        Returns:
            profile (str): Driver profile
        """
        # get driver trips
        trips = self.get_driver(uuid).trips
        print(len(trips))
        # must have at least 3 trips
        if len(trips) < 3:
            return None
        # get profiles dict
        prof_dict = current_app.config['PROFILES']
        # convert profile str to int
        profiles = [prof_dict[t.profile] for t in trips]
        # calculate gain loss func for all trips
        gain_loss = [np.log(y/x) for x, y in zip(profiles, profiles[1:])]
        # calculate driver volatility
        driver_volatility = np.std(gain_loss)
        # get most common profile
        # if 2/3 profiles are most common: choose de most sequently common
        # if there is no most sequently common or there is more than 1: choose most recent
        pfs, counts = np.unique(profiles, return_counts=True)
        highest_count = pfs[counts == counts.max()]
        if len(highest_count) > 1:
            l = [(i[0], len(list(i[1]))) for i in itertools.groupby(profiles)][::-1]
            driver_profile = max(l, key=lambda x:x[1])[0]
        else:
            driver_profile = highest_count[0]

        # create behavior message to warn if volatility is high
        if driver_volatility < 0.5:
            status = 'Consistent driver behavior over time.'
        else:
            status = 'Inconsistent driver behavior over time.'
        info = {
            'driver_profile': list(prof_dict.keys())[list(prof_dict.values()).index(driver_profile)],
            'behavior_status': {
                'status': status,
                'volatility': driver_volatility
            }
        }
        return info


driver_service = DriverService()
