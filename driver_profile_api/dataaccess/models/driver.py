# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.models.driver
-------

This module provides the Driver model.
"""

# packages
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid
# database
from driver_profile_api import db


class Driver(db.Model):
    """
    Driver ORM Model

    Attributes
    ----------
    id: Integer
        Database ID of the driver (primary key).
    uuid: UUID <CHAR>
        Web ID of the driver.
    created: DateTime
        Creation timestamp.

    Foreign key
    ----------
    client_id: Integer
        Associated Client id.

    Relationships
    ----------
    trips: Trip
        List of associated trips.
    """

    __tablename__ = 'driver'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUIDType(binary=False),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    name = db.Column(db.String(40), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # foreign key
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    # relationships
    trips = db.relationship('Trip', backref='driver')

    def __repr__(self):
        txt = "<Driver(id={}, uuid={})>"
        return txt.format(self.id, self.uuid)