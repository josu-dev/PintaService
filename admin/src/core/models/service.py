"""Model for service."""
from enum import Enum
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
from src.core.models.institution import Institution


class ServiceType(Enum):
    ANALYSIS = "analysis"
    CONSULTANCY = "consultancy"
    DEVELOPMENT = "development"


class Service(BaseModel):
    __tablename__ = "services"

    id: Mapped[IntPK] = mapped_column(init=False)
    name: Mapped[Str32]
    laboratory: Mapped[Str32]
    description: Mapped[Str512]
    keywords: Mapped[Str256]
    service_type: Mapped[ServiceType]
    enabled: Mapped[bool] = mapped_column(init=False, default=True)
    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
    # Relation with Institutions
    institutions: Mapped[List["Institution"]] = relationship(
        back_populates="service", default_factory=list
    )
