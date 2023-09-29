"""Model for service request."""
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.models.base import (
    BaseModel,
    CreatedAt,
    IntPK,
    Str32,
    Str512,
    UpdatedAt,
)


class Status(Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROCESS = "in_process"
    FINISHED = "finished"
    CANCELED = "canceled"


class ServiceRequest(BaseModel):
    __tablename__ = "service_requests"

    id: Mapped[IntPK] = mapped_column(init=False)
    title: Mapped[Str32]
    description: Mapped[Str512]
    status: Mapped[Status]

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
    # TODO Relations
    institution_id: Mapped[int] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(init=False)
    service_id: Mapped[int] = mapped_column(init=False)


class RequestNote(BaseModel):
    __tablename__ = "request_notes"

    id: Mapped[IntPK] = mapped_column(init=False)
    note: Mapped[Str512]

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
    # Relations
    service_request_id: Mapped[int] = mapped_column(init=False)
