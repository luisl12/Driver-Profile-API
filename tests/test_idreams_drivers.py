# -*- coding: utf-8 -*-
"""
tests.test_api
--------------

This module provides device endpoints tests for the API.

:copyright: (c) 2021 by CardioID Technologies Lda.
:license: All rights reserved.
"""

# packages
import pandas as pd
import requests
from datetime import datetime
import pytest
from os import environ, path
from dotenv import load_dotenv
# local
from driver_profile_api.utils.missing_values import fill_missing_values


# read .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


# API server
API_MODE = environ.get("API_MODE")
if API_MODE == 'dev':
    SRV = 'http://localhost:5000/'
elif API_MODE == 'test':
    SRV = 'http://localhost:5000/'
elif API_MODE == 'prod':
    SRV = 'http://localhost:5000/'
else:
    SRV = 'http://localhost:5000/'



def test_create_driver_and_trips():
    df = pd.read_csv('tests/trips_test_drivers_2022-05-14_2022-07-20.csv')
    assert df is not None

    df = fill_missing_values(df)

    unique_drivers = df['driver'].unique()
    print(unique_drivers, len(unique_drivers))
    """
    missing drivers = ['tnfkkL2scEX8gMw2d6ZoDq',
                       'onRztoYZ5reHb3B7YziGku',
                       'wzM4mbzZ5xD9pbX57rGyav']
    """

    for i, d in enumerate(unique_drivers):
        driver_trips = df[df['driver'] == d]
        # create driver
        name = 'Test i-DREAMS driver {}'.format(i+1)
        uuid = d
        driver = create_driver(name, uuid)
        # upload driver trips
        print('Driver:', driver['uuid'], 'N Trips:', driver_trips.shape)
        for tidx, t in driver_trips.iterrows():
            print('Driver:', driver['uuid'], 'Trip:', tidx)
            create_trip(driver['uuid'], t)

def create_driver(name, uuid):

    url = SRV + 'drivers'
    json = {
        'name': name,
        'uuid': uuid
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
    return out


def create_trip(driver, data):
    url = SRV + 'trips'

    json = {
        'driver': driver,
        'info': {
            'start': data['trip_start'].format('YYYY-MM-DD HH:mm:ss'),
            'end': data['trip_end'].format('YYYY-MM-DD HH:mm:ss'),
            'duration': data['duration'],
            'distance': data['distance'],
        },
        'data': {
            'n_ha': data['n_ha'],
            'n_ha_l': data['n_ha_l'],
            'n_ha_m': data['n_ha_m'],
            'n_ha_h': data['n_ha_h'],
            'n_hb': data['n_hb'],
            'n_hb_l': data['n_hb_l'],
            'n_hb_m': data['n_hb_m'],
            'n_hb_h': data['n_hb_h'],
            'n_hc': data['n_hc'],
            'n_hc_l': data['n_hc_l'],
            'n_hc_m': data['n_hc_m'],
            'n_hc_h': data['n_hc_h'],
            'fcw_time': data['fcw_time'],
            'hmw_time': data['hmw_time'],
            'ldw_time': data['ldw_time'],
            'pcw_time': data['pcw_time'],
            'n_pedestrian_dz': data['n_pedestrian_dz'],
            'n_tsr_level': data['n_tsr_level'],
            'n_tsr_level_0': data['n_tsr_level_0'],
            'n_tsr_level_1': data['n_tsr_level_1'],
            'n_tsr_level_2': data['n_tsr_level_2'],
            'n_tsr_level_3': data['n_tsr_level_3'],
            'n_tsr_level_4': data['n_tsr_level_4'],
            'n_tsr_level_5': data['n_tsr_level_5'],
            'n_tsr_level_6': data['n_tsr_level_6'],
            'n_tsr_level_7': data['n_tsr_level_7'],
            'n_brakes': data['n_brakes'],
            'speed': data['speed'],
            'n_fcw': data['n_fcw'],
            'n_hmw': data['n_hmw'],
            'n_ldw': data['n_ldw'],
            'n_ldw_left': data['n_ldw_left'],
            'n_ldw_right': data['n_ldw_right'],
            'n_pcw': data['n_pcw'],
            'n_fatigue_0': data['n_fatigue_0'],
            'n_fatigue_1': data['n_fatigue_1'],
            'n_fatigue_2': data['n_fatigue_2'],
            'n_fatigue_3': data['n_fatigue_3'],
            'n_headway__1': data['n_headway__1'],
            'n_headway_0': data['n_headway_0'],
            'n_headway_1': data['n_headway_1'],
            'n_headway_2': data['n_headway_2'],
            'n_headway_3': data['n_headway_3'],
            'n_overtaking_0': data['n_overtaking_0'],
            'n_overtaking_1': data['n_overtaking_1'],
            'n_overtaking_2': data['n_overtaking_2'],
            'n_overtaking_3': data['n_overtaking_3'],
            'n_speeding_0': data['n_speeding_0'],
            'n_speeding_1': data['n_speeding_1'],
            'n_speeding_2': data['n_speeding_2'],
            'n_speeding_3': data['n_speeding_3']
        }
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
    return out
