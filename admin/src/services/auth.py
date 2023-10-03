import secrets
from datetime import datetime, timedelta
from typing import TypedDict

from flask import request
from typing_extensions import Unpack

from src.core.db import db
from src.core.models.pre_regis_user import PreRegisterUser
from src.services.base import BaseService, BaseServiceError
from src.services.mail import MailService


class FullPreRegisterUser(TypedDict):
    firstname: str
    lastname: str
    email: str


class AuthServiceError(BaseServiceError):
    pass


class AuthService(BaseService):
    @classmethod
    def get_pre_user_by_email(cls, email: str):
        """returns the user according to email"""
        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.email == email)
            .first()
        )

    @classmethod
    def create_pre_user(cls, **kwargs: Unpack[FullPreRegisterUser]):
        """Create parcial user in database"""
        if AuthService.get_pre_user_by_email(kwargs["email"]):
            raise AuthServiceError(f"{kwargs['email']} Email already exists")
        token = secrets.token_urlsafe(64)
        user = PreRegisterUser(**kwargs, token=token)
        db.session.add(user)
        db.session.commit()
        MailService.send_mail(
            "Confirmacion de Registro",
            user.email,
            f"Finalice el registro entrando al siguiente link y completando con sus datos: <br/>{request.host_url}register?token={token}",  # noqa: E501
        )
        return user

    @classmethod
    def delete_pre_user(cls, token: str):  # consultar
        """delete pre-user"""

        db.session.query(PreRegisterUser).where(
            PreRegisterUser.token == token
        ).delete()
        db.session.commit()

    @classmethod
    def get_pre_user_by_token(cls, token: str):
        """check if the token is valid"""

        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.token == token)
            .first()
        )

    @classmethod
    def exist_pre_user_with_email(cls, email: str):
        """check if the token is valid"""

        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.email == email)
            .first()
            is not None
        )

    @classmethod
    def token_expired(cls, token_date: datetime):
        current_date = datetime.now()
        difference = current_date - token_date
        one_day = timedelta(days=1)
        return difference > one_day
