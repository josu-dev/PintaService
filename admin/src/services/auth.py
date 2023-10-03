import secrets
from typing import TypedDict

from typing_extensions import Unpack

from src.core.bcrypt import bcrypt
from src.core.db import db
from src.core.models.pre_regis_user import PreRegisterUser
from src.core.models.user import User
from src.services.base import BaseService, BaseServiceError


class FullPreRegisterUser(TypedDict):
    firstname: str
    lastname: str
    email: str


class FullLoginUser(TypedDict):
    email: str
    password: str


class AuthServiceError(BaseServiceError):
    pass


class AuthService(BaseService):
    @classmethod
    def get_pre_register_user_by_email(cls, email: str):
        """returns the user according to email"""
        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.email == email)
            .first()
        )

    @classmethod
    def get_user_by_email(cls, email: str):
        """returns the user according to email"""
        return db.session.query(User).filter(User.email == email).first()

    @classmethod
    def validate_email_password(cls, email: str, password: str):
        """Check if the mail and password are valid"""
        user = cls.get_user_by_email(email)

        if user and bcrypt.check_password_hash(
            user.password, password.encode("utf-8")
        ):
            return user

        return None

    @classmethod
    def create_pre_user(cls, **kwargs: Unpack[FullPreRegisterUser]):
        """Create parcial user in database"""
        if AuthService.get_user_by_email(kwargs["email"]):
            raise AuthServiceError(f"{kwargs['email']} Email already exists")
        token = secrets.token_urlsafe(64)
        user = PreRegisterUser(**kwargs, token=token)

        db.session.add(user)
        db.session.commit()

    @classmethod
    def delete_pre_user(cls, token: str):  # consultar
        """delete pre-user"""

        db.session.query(PreRegisterUser).where(
            PreRegisterUser.token == token
        ).delete()
        db.session.commit()

    @classmethod
    def get_pre_user(cls, token: str):
        """check if the token is valid"""

        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.token == token)
            .first()
        )
