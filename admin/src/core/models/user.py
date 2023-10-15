"""Model for user."""
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.enums import DocumentTypes, GenderOptions
from src.core.models.base import (
    BaseModel,
    IntPK,
    Str32,
    Str64,
    Str256,
    Timestamp,
)


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[IntPK] = mapped_column(init=False)

    firstname: Mapped[Str32]
    lastname: Mapped[Str32]
    password: Mapped[Str256]
    email: Mapped[Str64]
    username: Mapped[Str32]

    document_type: Mapped[DocumentTypes]
    document_number: Mapped[Str32]

    gender: Mapped[GenderOptions]
    gender_other: Mapped[Optional[Str32]]

    address: Mapped[Str256]
    phone: Mapped[Str32]
    is_active: Mapped[bool] = mapped_column(init=False, default=True)

    institutions = relationship(  # type: ignore
        "Institution", secondary="institution_user", back_populates="users"
    )

    created_at: Mapped[Timestamp] = mapped_column(init=False)
    updated_at: Mapped[Timestamp] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
