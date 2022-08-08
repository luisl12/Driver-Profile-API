# -*- coding: utf-8 -*-
"""
tests.test_api_endpoints
--------------

This module provides tests to the API endpoints.
"""

# packages
import requests
import pytest
from os import environ, path
from dotenv import load_dotenv


# read .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '../.env'))


# API server
API_MODE = environ.get("API_MODE")
if API_MODE == 'dev':
    SRV = environ.get("DEV_API_SRV")
elif API_MODE == 'test':
    SRV = environ.get("TEST_API_SRV")
elif API_MODE == 'prod':
    SRV = environ.get("TEST_API_SRV")
else:
    SRV = environ.get("DEV_API_SRV")

USERNAME = 'Test username'
CLIENT = 'Test client'
IDREAMS_UUIDS = ['4q5n6yzRgPx46DbZgbPT5s', 'anTgCLZSv5JMpDakadVcVG']
DRIVER_UUID = ''
CLIENT_UUID = ''
FLEET_UUID = ''


@pytest.mark.dependency
def test_create_driver():
    url = SRV + 'drivers'
    json = {
        'name': USERNAME
    }
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.post(url, json=json, headers=headers)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, dict)
    assert 'name' in out
    assert 'uuid' in out
    global DRIVER_UUID
    DRIVER_UUID = out['uuid']


@pytest.mark.dependency
def test_create_client():
    url = SRV + 'clients'

    json = {
        'client': CLIENT,
        'fleets': ['Test fleet 1']
    }
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.post(url, json=json, headers=headers)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, dict)
    assert 'uuid' in out
    assert 'name' in out
    assert 'drivers' in out
    assert 'fleets' in out
    global CLIENT_UUID
    global FLEET_UUID
    CLIENT_UUID = out['uuid']
    FLEET_UUID = out['fleets'][0]


@pytest.mark.dependency(depends=['test_create_driver', 'test_create_client'])
def test_create_trip():
    url = SRV + 'trips'

    infos = [
        {
            'start': '2022-02-01T07:28:25+00:00',
            'end': '2022-02-01T07:41:11+00:00',
            'duration': 766,
            'distance': 6.44472,
        },
        {
            'start': '2022-02-01T08:08:59+00:00',
            'end': '2022-02-01T08:51:27+00:00',
            'duration': 2548,
            'distance': 44.4533,
        }
    ]
    for i, info in enumerate(infos):
        json = {
            'driver': DRIVER_UUID,
            'fleet': FLEET_UUID,
            'info': info,
            'idreams_uuid': IDREAMS_UUIDS[i]
        }
        headers = {
            'Content-Type': 'application/json',
        }
        resp = requests.post(url, json=json, headers=headers)
        assert resp.ok
        out = resp.json()
        assert isinstance(out, dict)
        assert 'uuid' in out
        assert 'start' in out
        assert 'end' in out
        assert 'duration' in out
        assert 'distance' in out
        assert 'profile' in out
        assert 'fleet' in out


def test_get_clients():
    url = SRV + 'clients'
    resp = requests.get(url)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, list)


def test_get_drivers():
    url = SRV + 'drivers'
    resp = requests.get(url)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, list)


@pytest.mark.dependency(depends=['test_create_driver'])
def test_get_driver_trips():
    url = SRV + 'drivers/' + DRIVER_UUID + '/trips'
    resp = requests.get(url)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, list)


@pytest.mark.dependency(depends=['test_create_client'])
def test_get_fleet_trips():
    url = SRV + 'clients/' + CLIENT_UUID + '/fleets/' + FLEET_UUID + '/trips'
    resp = requests.get(url)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, list)


@pytest.mark.dependency(depends=['test_create_driver'])
def test_get_driver_profile():
    url = SRV + 'drivers/' + DRIVER_UUID + '/profile'
    resp = requests.get(url)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, dict)
    assert 'behavior_status' in out
    assert 'driver_profile' in out


@pytest.mark.dependency(depends=['test_create_client'])
def test_get_fleet_profile():
    url = SRV + 'clients/' + CLIENT_UUID + '/fleets/' + FLEET_UUID + '/profile'
    resp = requests.get(url)
    assert resp.ok
    out = resp.json()
    assert isinstance(out, dict)
    assert 'behavior_status' in out
    assert 'fleet_profile' in out


@pytest.mark.dependency(depends=['test_create_client', 'test_create_driver'])
def test_add_client_drivers():
    url = SRV + 'clients/' + CLIENT_UUID + '/drivers'
    json = {
        'drivers': [DRIVER_UUID],
    }
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.patch(url, json=json, headers=headers)
    assert resp.ok


@pytest.mark.dependency(depends=['test_create_client'])
def test_add_client_fleets():
    url = SRV + 'clients/' + CLIENT_UUID + '/fleets'
    json = {
        'fleets': ['Test fleet 2'],
    }
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.patch(url, json=json, headers=headers)
    assert resp.ok