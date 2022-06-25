# -*- coding: utf-8 -*-
"""
driver_profile_api.wsgi
-----------------

This module runs the API.
"""

# packages
from os import environ, path
from dotenv import load_dotenv
# Flask app factory
from driver_profile_api import create_app


# read .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# get API mode
API_MODE = environ.get('API_MODE')

# choose config class
if API_MODE == 'dev':
    config = "config.DevConfig"
elif API_MODE == 'test':
    config = "config.TestConfig"
elif API_MODE == 'prod':
    config = "config.ProdConfig"
else:
    # use dev config
    config = "config.DevConfig"

app = create_app(config)  # call from wsgi server

if __name__ == "__main__":
    app.run(host='0.0.0.0')
