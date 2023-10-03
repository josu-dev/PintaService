from typing import List, Optional, TypedDict

from typing_extensions import Unpack

from src.core.bcrypt import bcrypt
from src.core.db import db
from src.core.models.user import User
from src.services.base import BaseService, BaseServiceError


class PartialUserConfig(TypedDict):
    firstname: str
    lastname: str
    password: str
    email: str
    username: str
    document_type: str
    document_number: str
    gender: str
    address: str
    phone: str
    gender_other: Optional[str]


class UserServiceError(BaseServiceError):
    pass


class UserService(BaseService):
    """Create, read, update and delete users."""

    UserServiceError = UserServiceError

    @classmethod
    def get_users(cls) -> List[User]:
        """Get all users from database"""
        return db.session.query(User).all()

    @classmethod
    def get_user(cls, user_id: int):
        """Get an user from database"""
        db.session.get(User, user_id)

    @classmethod
    def update_user(cls, user_id: int, **kwargs: Unpack[PartialUserConfig]):
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
        **kwargs: Unpack[PartialUserConfig],
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

    # TODO Filter by email and Active/unactive
