import typing as t

import typing_extensions as te
from sqlalchemy import exc, insert, select, update

from src.core.db import db
from src.core.models.site import SiteConfig, defaultSiteConfig
from src.services.base import BaseService, BaseServiceError, filter_nones


class PartialSiteConfig(t.TypedDict):
    page_size: te.NotRequired[int]
    contact_info: te.NotRequired[str]
    maintenance_active: te.NotRequired[bool]
    maintenance_message: te.NotRequired[str]


class SiteServiceError(BaseServiceError):
    pass


class SiteService(BaseService):
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
        cls, **kwargs: te.Unpack[PartialSiteConfig]
    ) -> SiteConfig:
        try:
            site_config = db.session.execute(
                update(SiteConfig)
                .values(**filter_nones(kwargs))
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
