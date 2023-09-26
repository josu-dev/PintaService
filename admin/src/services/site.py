from typing import Union

from sqlalchemy import select, update

from src.core.db import db
from src.core.models.site import SiteConfig, defaultSiteConfig
from src.services.base import BaseService, ServiceError


class SiteService(BaseService):
    _cache: Union[SiteConfig, None] = None

    @staticmethod
    def default() -> SiteConfig:
        return defaultSiteConfig()

    @classmethod
    def get_site_config(cls) -> SiteConfig:
        site_config = db.session.execute(select(SiteConfig)).scalar()
        if site_config is None:
            raise ServiceError("No site config loaded")

        cls._cache = site_config
        return site_config

    @classmethod
    def update_site_config(
        cls,
        id: Union[int, None] = None,
        page_size: Union[int, None] = None,
        contact_info: Union[str, None] = None,
        maintenance_active: Union[bool, None] = None,
        maintenance_message: Union[str, None] = None,
    ) -> SiteConfig:
        if id is None:
            id = SiteService.get_site_config().id
        values = {}
        if page_size is not None:
            values["page_size"] = page_size
        if contact_info is not None:
            values["contact_info"] = contact_info
        if maintenance_active is not None:
            values["maintenance_active"] = maintenance_active
        if maintenance_message is not None:
            values["maintenance_message"] = maintenance_message

        site_config = db.session.execute(
            update(SiteConfig)
            .where(SiteConfig.id == id)
            .values(**values)
            .returning(SiteConfig)
        ).scalar()
        db.session.commit()

        cls._cache = site_config

        if site_config is None:
            raise ServiceError("No site config loaded")

        return site_config

    @classmethod
    def maintenance_active(cls) -> bool:
        if cls._cache is None:
            cls.get_site_config()
            if cls._cache is None:
                return False

        return cls._cache.maintenance_active

    @classmethod
    def maintenance_message(cls) -> str:
        if cls._cache is None:
            cls.get_site_config()
            if cls._cache is None:
                return ""

        return cls._cache.maintenance_message
