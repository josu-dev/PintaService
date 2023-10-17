"""Model for service request."""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.enums import RequestStatus
from src.core.models.base import (
    BaseModel,
    CreatedAt,
    IntPK,
    Str32,
    Str512,
    UpdatedAt,
)


class ServiceRequest(BaseModel):
    __tablename__ = "service_requests"

    id: Mapped[IntPK] = mapped_column(init=False)
    title: Mapped[Str32]
    description: Mapped[Str512]
    status: Mapped[RequestStatus]

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )

    institution_id: Mapped[int]
    user_id: Mapped[int]
    service_id: Mapped[int]


class RequestNote(BaseModel):
    __tablename__ = "request_notes"

    id: Mapped[IntPK] = mapped_column(init=False)
    note: Mapped[Str512]

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )

    service_request_id: Mapped[int]
