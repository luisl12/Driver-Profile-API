# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.services.idreams_service
-------

This module provides the i-DREAMS service.
"""

# packages
import requests
from os import environ, path
from dotenv import load_dotenv
# utils
from ...utils.utils import InvalidAPIUsage


class iDreamsService:
    """
    i-DREAMS Service
    """

    def __init__(self, srv, token):
        """
        i-DREAMS service constructor

        Args:
            srv (str): CardioID API server url
        """
        self.srv = srv
        self.token = token

    def get_trip_data(self, uuid):
        """
        Get trip data by uuid

        Args:
            uuid (str): Trip UUID

        Returns:
            data (dict): Retrieved trip data
        """
        url = self.srv + '/idreams/trip/data'

        query = {
            'uuid': uuid,
        }

        headers = {
            'Auth-Token': self.token,
            'Content-Type': 'application/json',
        }

        try:
            resp = requests.post(url, headers=headers, json=query)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            raise InvalidAPIUsage("i-DREAMS Server Error.", status_code=500)
        except requests.exceptions.ConnectionError as errc:
            raise InvalidAPIUsage("i-DREAMS Server Error.", status_code=500)
        except requests.exceptions.Timeout as errt:
            raise InvalidAPIUsage("i-DREAMS Server Error.", status_code=500)
        except requests.exceptions.RequestException as err:
            raise InvalidAPIUsage("i-DREAMS Server Error.", status_code=500)

        if not resp.ok:
            raise InvalidAPIUsage("i-DREAMS Server Error.", status_code=500)

        data = resp.json()
        return data


# read .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

srv = environ.get('DEV_IDREAMS_SRV')
token = environ.get('DEV_IDREAMS_TOKEN')
idreams_service = iDreamsService(srv, token)
