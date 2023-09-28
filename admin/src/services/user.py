from typing import List, Optional, TypedDict

from typing_extensions import Unpack

from src.core.db import db
from src.core.models.user import User
from src.services.base import BaseService


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


class UserService(BaseService):
    """Create, read, update and delete users."""

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
        user = User(**kwargs)
        if UserService.get_by_email(kwargs["email"]):
            raise ValueError("Email already exists")
        if UserService.get_by_username(kwargs["username"]):
            raise ValueError("Username already exists")
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
