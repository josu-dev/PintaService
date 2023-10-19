"""Model for service."""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.enums import ServiceType
from src.core.models.base import (
    BaseModel,
    CreatedAt,
    IntPK,
    Str32,
    Str256,
    Str512,
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

    institution_id: Mapped[int]

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
