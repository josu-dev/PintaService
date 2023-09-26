from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.models.base import BaseModel, IntPK, Str256, Str512, Timestamp


class SiteConfig(BaseModel):
    __tablename__ = "site_config"

    id: Mapped[IntPK] = mapped_column(init=False)
    page_size: Mapped[int]
    contact_info: Mapped[Str256]
    maintenance_active: Mapped[bool]
    maintenance_message: Mapped[Str512]
    # maintenance_finished_at: Mapped[Timestamp] = mapped_column(
    #     init=False, nullable=True
    # )
    created_at: Mapped[Timestamp] = mapped_column(init=False)
    updated_at: Mapped[Timestamp] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )


def defaultSiteConfig():
    return SiteConfig(
        page_size=10,
        contact_info="",
        maintenance_active=False,
        maintenance_message="",
    )


def seed_site_config(db: SQLAlchemy):
    new_config = defaultSiteConfig()
    db.session.add(new_config)
    db.session.commit()
