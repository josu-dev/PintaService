"""Model for service."""
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.enums import ServiceType
from src.core.models.base import (
    BaseModel,
    CreatedAt,
    IntPK,
    Str32,
    Str256,
    Str512,
    Timestamp,
    UpdatedAt,
)


class Service(BaseModel):
    __tablename__ = "services"

    id: Mapped[IntPK] = mapped_column(init=False)
    name: Mapped[Str32]
    laboratory: Mapped[Str32]
    description: Mapped[Str512]
    keywords: Mapped[Str256]
    service_type: Mapped[ServiceType]
    enabled: Mapped[bool] = mapped_column(init=False, default=True)

    institutions = relationship(  # type:ignore
        "Institution",
        secondary="institution_service",
        back_populates="services",
    )

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )


class InstitutionService(BaseModel):
    __tablename__ = "institution_service"

    id: Mapped[IntPK] = mapped_column(init=False)

    service_id = Column(Integer, ForeignKey("services.id"))
    institution_id = Column(Integer, ForeignKey("institutions.id"))

    created_at: Mapped[Timestamp] = mapped_column(init=False)
    updated_at: Mapped[Timestamp] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
