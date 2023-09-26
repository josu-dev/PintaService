"""Model for user."""
from typing import List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.models.base import BaseModel, IntPK, Str32, Str256, Timestamp
from src.core.models.institution import Institution


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[IntPK] = mapped_column(init=False)

    firstname: Mapped[Str32]
    lastname: Mapped[Str32]
    password: Mapped[Str32]
    email: Mapped[Str32]
    username: Mapped[Str32]
    document_type: Mapped[Str32]
    document_number: Mapped[Str32]
    gender: Mapped[Str32]
    gender_other: Mapped[Optional[Str32]]
    address: Mapped[Str256]
    phone: Mapped[Str32]
    is_active: Mapped[bool] = mapped_column(init=False, default=True)

    created_at: Mapped[Timestamp] = mapped_column(init=False)
    updated_at: Mapped[Timestamp] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
    # Relation with institution
    institutions: Mapped[List["Institution"]] = relationship(
        back_populates="user", default_factory=list
    )


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    id: Mapped[IntPK] = mapped_column(init=False)
    user_id: Mapped[IntPK]
    institution_id: Mapped[IntPK]
    role: Mapped[Str32]


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"

    id: Mapped[IntPK] = mapped_column(init=False)
    role_id: Mapped[IntPK]
    permission: Mapped[Str32]
