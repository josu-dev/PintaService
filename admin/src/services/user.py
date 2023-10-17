import typing as t

import typing_extensions as te
from sqlalchemy import and_

from src.core.bcrypt import bcrypt
from src.core.db import db
from src.core.enums import DocumentTypes, GenderOptions
from src.core.models.auth import SiteAdmin
from src.core.models.user import User
from src.services.base import BaseService, BaseServiceError


class UserParams(t.TypedDict):
    firstname: str
    lastname: str
    password: str
    email: str
    username: str
    document_type: DocumentTypes
    document_number: str
    gender: GenderOptions
    address: str
    phone: str
    gender_other: te.NotRequired[str]


class UserUpdateParams(t.TypedDict):
    firstname: str
    lastname: str
    document_type: DocumentTypes
    document_number: str
    gender: GenderOptions
    address: str
    phone: str
    gender_other: te.NotRequired[str]


class UserServiceError(BaseServiceError):
    pass


class UserService(BaseService):
    """Create, read, update and delete users."""

    UserServiceError = UserServiceError

    @classmethod
    def get_users(
        cls, page: int = 1, per_page: int = 10
    ) -> t.Tuple[t.List[User], int]:
        """Get  users from database"""
        subquery = db.session.query(SiteAdmin.user_id)
        users = (
            db.session.query(User)
            .filter(~User.id.in_(subquery))
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        total = db.session.query(User).count() - subquery.count()
        return users, total

    @classmethod
    def get_user(cls, user_id: int):
        """Get an user from database"""
        return db.session.get(User, user_id)

    @classmethod
    def update_user(cls, user_id: int, **kwargs: te.Unpack[UserUpdateParams]):
        """Update user in the database"""
        user = db.session.query(User).get(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        return None

    @classmethod
    def delete_user(cls, user_id: int):
        """Delete user from database"""
        user = db.session.query(User).get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def create_user(
        cls,
        **kwargs: te.Unpack[UserParams],
    ):
        """Create user in database"""
        if UserService.get_by_username(kwargs["username"]):
            raise UserServiceError("Username already exists")

        hash = bcrypt.generate_password_hash(
            kwargs["password"].encode("utf-8")
        )
        kwargs["password"] = hash.decode("utf-8")
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def get_by_email(cls, email: str):
        """Get user by email"""
        return db.session.query(User).filter(User.email == email).first()

    @classmethod
    def get_by_username(cls, username: str):
        """Get user by username"""
        return db.session.query(User).filter(User.username == username).first()

    @classmethod
    def toggle_active(cls, id: int):
        """Toggle user active status"""
        user = db.session.query(User).get(id)
        if user:
            user.is_active = not user.is_active
            db.session.commit()
            return user
        return None

    @classmethod
    def validate_email_password(cls, email: str, password: str):
        """Check if the mail and password are valid"""
        user = cls.get_by_email(email)

        if user and bcrypt.check_password_hash(
            user.password, password.encode("utf-8")
        ):
            return user

        return None

    @classmethod
    def exist_user_with_email(cls, email: str):
        """check if the email is valid"""

        return (
            db.session.query(User).filter(User.email == email).first()
            is not None
        )

    @classmethod
    def exist_user_with_username(cls, username: str):
        """check if the username is valid"""

        return (
            db.session.query(User).filter(User.username == username).first()
            is not None
        )

    @classmethod
    def filter_users_by_email_and_active(
        cls,
        email: t.Union[str, None],
        active: t.Union[str, None],
        page: int = 1,
        per_page: int = 10,
    ) -> t.Tuple[t.List[User], int]:
        query = db.session.query(User)

        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))

        if active == "1":
            query = query.filter(User.is_active)
        elif active == "0":
            query = query.filter(~User.is_active)

        query = query.join(SiteAdmin, and_(User.id != SiteAdmin.user_id))

        total = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()

        return users, total
