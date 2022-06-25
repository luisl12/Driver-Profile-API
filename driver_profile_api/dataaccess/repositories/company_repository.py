# -*- coding: utf-8 -*-
"""
driver_profile_api.dataaccess.repositories.company_repository
-------

This module provides the company repository.
"""

# packages
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
# models
from ..models.company import Company
from driver_profile_api import db


class CompanyRepository:
    """
    Company Repository
    """

    def __init__(self, model):
        """
        Company repository constructor

        Args:
            model (db.model): Company model
        """
        self.model = model

    def get_company(self, uuid):
        """
        Get company by uuid

        Args:
            uuid (UUID): Company UUID

        Returns:
            Company: Company instance
        """
        return (
            db.session.query(self.model)
            .filter_by(uuid=uuid)
            .first()
        )

    def create_company(self, name, uuid=None):
        """
        Create new company

        Args:
            name (str): Company name
            uuid (str, optional): Company UUID. Defaults to None.

        Returns:
            company (Company): Company created
        """
        try:
            if uuid:
                driver = Company(uuid=uuid, name=name)
            else:
                driver = Company(name=name)
            db.session.add(driver)
            db.session.commit()
        except SQLAlchemyError as err:
            current_app.logger.exception(err)
            db.session.rollback()
            return False
        else:
            return driver

company_rep = CompanyRepository(Company)
