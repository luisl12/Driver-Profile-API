# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.models.trip
-------

This module provides the Trip model.
"""

# packages
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid
# database
from driver_profile_api import db


class Trip(db.Model):
    """
    Trip ORM Model

    Attributes
    ----------
    id: Integer
        Database ID of the driver (primary key).
    uuid: UUID <CHAR>
        Web ID of the driver.
    distance: Float
        Trip distance in meters.
    duration: Float
        Trip duration in seconds.
    start: DateTime
        Trip start timestamp.
    end: DateTime
        Trip end timestamp.
    created: DateTime
        Creation timestamp.

    Foreign keys
    ----------
    driver_id: Integer
        Associated Driver id.
    fleet_id: Integer
        Associated Fleet id.
    """

    __tablename__ = 'trip'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUIDType(binary=False),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    distance = db.Column(db.Float)
    duration = db.Column(db.Float)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    profile = db.Column(db.String(15))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # foreign keys
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    fleet_id = db.Column(db.Integer, db.ForeignKey('fleet.id'))
    
    def __repr__(self):
        txt = "<Trip(id={}, uuid={})>"
        return txt.format(self.id, self.uuid)