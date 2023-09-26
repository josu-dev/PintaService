"""Model for institution."""
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.models.base import (
    BaseModel,
    CreatedAt,
    IntPK,
    Str32,
    Str256,
    Str512,
    UpdatedAt,
)
from src.core.models.service import Service
from src.core.models.service_requests import ServiceRequest
from src.core.models.user import User


class Institution(BaseModel):
    __tablename__ = "institutions"

    id: Mapped[IntPK] = mapped_column(init=False)

    name: Mapped[Str32]
    information: Mapped[Str512]
    address: Mapped[Str256]
    location: Mapped[Str256]
    web: Mapped[Str256]
    keywords: Mapped[Str256]
    email: Mapped[Str256]
    days_and_opening_hours: Mapped[Str256]
    enabled: Mapped[bool] = mapped_column(init=False, default=True)

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
    # Relation with user
    users: Mapped[List["User"]] = relationship(
        back_populates="institution", default_factory=list
    )
    # Relation with his services
    services: Mapped[List["Service"]] = relationship(
        back_populates="institution", default_factory=list
    )
    # Relation with his service requests
    service_requests: Mapped[List["ServiceRequest"]] = relationship(
        back_populates="institution", default_factory=list
    )
