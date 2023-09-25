from typing import Union

from sqlalchemy import select, update

from src.core.db import db
from src.core.models.site import SiteConfig
from src.services.base import BaseService, ServiceError


class SiteService(BaseService):
    @staticmethod
    def default() -> SiteConfig:
        return SiteConfig(
            page_size=10,
            contact_info="",
            maintenance_active=False,
            maintenance_message="",
        )

    @staticmethod
    def get_site_config() -> SiteConfig:
        site_config = db.session.execute(select(SiteConfig)).scalar()
        if site_config is None:
            raise ServiceError("No site config loaded")

        return site_config

    @staticmethod
    def update_site_config(
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
        if site_config is None:
            raise ServiceError("No site config loaded")

        return site_config
