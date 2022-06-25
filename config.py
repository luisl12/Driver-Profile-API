# -*- coding: utf-8 -*-
"""
driver_profile_api.config
-----------------

Defines Flask app environment variables.
"""

# packages
from os import environ, path
from dotenv import load_dotenv


# read .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """
    Base Flask App Configuration
    """
    DEBUG = True
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB Request max size
    # JWT_ALGORITHM = environ.get('JWT_ALGORITHM')
    # JWT_DECODE_ALGORITHMS = [environ.get('JWT_DECODE_ALGORITHMS')]
    # JWT_PUBLIC_KEY = open('D:/Estagio/workspace/Tests/.ssh/public.pub').read()
    # JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(
    #     minutes=int(environ.get('JWT_ACCESS_TOKEN_EXPIRES'))
    # )


class DevConfig(Config):
    """
    Development Flask App Configuration
    """
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}' \
        .format(environ.get("DEV_DB_DRIVER"),
                environ.get("DEV_DB_USERNAME"),
                environ.get("DEV_DB_PASSWORD"),
                environ.get("DEV_DB_HOST"),
                environ.get("DEV_DB_PORT"),
                environ.get("DEV_DB_NAME"))


class TestConfig(Config):
    """
    Test Flask App Configuration
    """
    ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}' \
        .format(environ.get("TEST_DB_DRIVER"),
                environ.get("TEST_DB_USERNAME"),
                environ.get("TEST_DB_PASSWORD"),
                environ.get("TEST_DB_HOST"),
                environ.get("TEST_DB_PORT"),
                environ.get("TEST_DB_NAME"))


class ProdConfig(Config):
    """
    Production Flask App Configuration
    """
    ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}' \
        .format(environ.get("PROD_DB_DRIVER"),
                environ.get("PROD_DB_USERNAME"),
                environ.get("PROD_DB_PASSWORD"),
                environ.get("PROD_DB_HOST"),
                environ.get("PROD_DB_PORT"),
                environ.get("PROD_DB_NAME"))
