import typing as t

import typing_extensions as te
from sqlalchemy import exc, insert, select, update

from src.core.db import db
from src.core.models.site import SiteConfig, defaultSiteConfig
from src.services.base import BaseService, BaseServiceError
from src.utils import funcs


class SiteConfigParams(t.TypedDict):
    page_size: int
    contact_info: str
    maintenance_active: bool
    maintenance_message: str


class SiteConfigPartialParams(t.TypedDict):
    page_size: te.NotRequired[int]
    contact_info: te.NotRequired[str]
    maintenance_active: te.NotRequired[bool]
    maintenance_message: te.NotRequired[str]


class SiteServiceError(BaseServiceError):
    pass


class SiteService(BaseService):
    """Service for handling site config.

    This service is used for updating and retrieving the site config.
    """

    SiteServiceError = SiteServiceError

    @staticmethod
    def default_site_config() -> SiteConfig:
        return defaultSiteConfig()

    @classmethod
    def _on_missing_site_config(cls) -> SiteConfig:
        site_config = defaultSiteConfig()
        return site_config

    @classmethod
    def get_site_config(cls) -> SiteConfig:
        """Gets the site config.

        If the site config is missing, it will be created with the default.

        Raises:
            SiteServiceError: If the site config could not be retrieved.
        """
        try:
            site_config = db.session.execute(select(SiteConfig)).scalar()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            raise SiteServiceError(f"Could not retrieve site config: {e.code}")

        if site_config is None:
            return cls._on_missing_site_config()

        return site_config

    @classmethod
    def update_site_config(
        cls, **kwargs: te.Unpack[SiteConfigPartialParams]
    ) -> SiteConfig:
        """Updates the site config.

        If the site config is missing, it will be created with the default.

        Raises:
            SiteServiceError: If the site config could not be updated.
        """
        try:
            site_config = db.session.execute(
                update(SiteConfig)
                .values(**funcs.filter_nones(kwargs))
                .returning(SiteConfig)
            ).scalar()
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            raise SiteServiceError(f"Could not update site config: {e.code}")

        if site_config is None:
            try:
                site_config = db.session.execute(
                    insert(SiteConfig).values(**kwargs).returning(SiteConfig)
                ).scalar()
                db.session.commit()
            except exc.SQLAlchemyError as e:
                db.session.rollback()
                raise SiteServiceError(
                    f"Could not insert site config on missing config: {e.code}"
                )

            if site_config is None:
                raise SiteServiceError(
                    "Could not retrieve site config after insert"
                )

        return site_config

    @classmethod
    def maintenance_active(cls) -> bool:
        return cls.get_site_config().maintenance_active

    @classmethod
    def maintenance_message(cls) -> str:
        return cls.get_site_config().maintenance_message
