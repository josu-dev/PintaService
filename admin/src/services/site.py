from typing import TypedDict

from sqlalchemy import select, update
from typing_extensions import NotRequired, Unpack

from src.core.db import db
from src.core.models.site import SiteConfig, defaultSiteConfig
from src.services.base import BaseService, BaseServiceError, filter_nones


class PartialSiteConfig(TypedDict):
    page_size: NotRequired[int]
    contact_info: NotRequired[str]
    maintenance_active: NotRequired[bool]
    maintenance_message: NotRequired[str]


class SiteService(BaseService):
    @staticmethod
    def default() -> SiteConfig:
        return defaultSiteConfig()

    @classmethod
    def get_site_config(cls) -> SiteConfig:
        site_config = db.session.execute(select(SiteConfig)).scalar()
        if site_config is None:
            raise BaseServiceError("No site config loaded")

        return site_config

    @classmethod
    def update_site_config(
        cls, **kwargs: Unpack[PartialSiteConfig]
    ) -> SiteConfig:
        site_config = db.session.execute(
            update(SiteConfig)
            .values(**filter_nones(kwargs))
            .returning(SiteConfig)
        ).scalar()
        db.session.commit()

        if site_config is None:
            raise BaseServiceError("No site config loaded")

        return site_config

    @classmethod
    def maintenance_active(cls) -> bool:
        return cls.get_site_config().maintenance_active

    @classmethod
    def maintenance_message(cls) -> str:
        return cls.get_site_config().maintenance_message
