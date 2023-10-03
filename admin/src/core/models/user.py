"""Model for user."""
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

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
    document_type: Mapped[Str32]
    document_number: Mapped[Str32]
    gender: Mapped[Str32]
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


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    id: Mapped[IntPK] = mapped_column(init=False)
    user_id: Mapped[int]
    institution_id: Mapped[int]
    role: Mapped[Str32]


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"

    id: Mapped[IntPK] = mapped_column(init=False)
    role_id: Mapped[int]
    permission: Mapped[Str32]


def seed_site_users(db: SQLAlchemy):
    from src.services.user import UserService

    UserService.create_user(
        firstname="Luciano Ariel",
        lastname="Lopez",
        password="1234",
        email="waderlax@hotmail.com",
        username="waderlax",
        document_type="DNI",
        document_number="40188236",
        gender="hombre",
        gender_other="tal vez",
        address="155",
        phone="2213169050",
    )
    UserService.create_user(
        firstname="Luciano",
        lastname="Lopez",
        password="1234",
        email="lucholopezlp@hotmail.com",
        username="lucho",
        document_type="DNI",
        document_number="40188236",
        gender="mujer",
        gender_other="",
        address="155",
        phone="2213169050",
    )

    UserService.create_user(
        firstname="Franco",
        lastname="Cirielli",
        password="1234",
        email="franco@hotmail.com",
        username="francry",
        document_type="DNI",
        document_number="25683652",
        gender="dudoso",
        gender_other="tal vez",
        address="15 y 47",
        phone="2355572726",
    )

    db.session.commit()
