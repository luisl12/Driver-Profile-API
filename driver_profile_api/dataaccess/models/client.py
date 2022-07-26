# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.models.client
-------

This module provides the Client model.
"""

# packages
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid
# database
from driver_profile_api import db


class Client(db.Model):
    """
    Client ORM Model

    Attributes
    ----------
    id: Integer
        Database ID of the client (primary key).
    uuid: UUID <CHAR>
        Web ID of the client.
    name: String
        Company name.
    created: DateTime
        Creation timestamp.

    Relationships
    ----------
    drivers: Driver
        List of associated drivers.
    fleets: Fleet
        List of associated fleets.
    """

    __tablename__ = 'client'

    # attributes
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUIDType(binary=False),
        unique=True,
        nullable=False,
        default=uuid.uuid4,
    )
    name = db.Column(db.String(40), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # relationships
    drivers = db.relationship('Driver', backref='client')
    fleets = db.relationship('Fleet', backref='client')

    def __repr__(self):
        txt = "<Client(id={}, uuid={}, name={})>"
        return txt.format(self.id, self.uuid, self.name)