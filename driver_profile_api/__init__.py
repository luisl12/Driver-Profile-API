# -*- coding: utf-8 -*-
"""
driver_profile_api
-------

This package provides the API for the driver profile classification.
"""

from .__version__ import __version__
# packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager


# initialize sqlalchemy and migrate
db = SQLAlchemy()
migrate = Migrate()
# jwt = JWTManager()


def create_app(config_class):
    """
    Creates application factory

    Args:
        config_class (str): Configuration Class name

    Returns:
        Flask: Flask App
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # jwt.init_app(app)

    # register blueprints
    from .presentation.home_blueprint import home_bp
    app.register_blueprint(home_bp)

    from .presentation.trips_blueprint import trips_bp
    app.register_blueprint(trips_bp)

    from .presentation.drivers_blueprint import drivers_bp
    app.register_blueprint(drivers_bp)

    from .presentation.errors_blueprint import errors_bp
    app.register_blueprint(errors_bp)

    # create DB tables from ORM if they dont exist
    with app.app_context():
        db.create_all()

    return app
