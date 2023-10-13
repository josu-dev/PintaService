import secrets
import typing as t
from datetime import datetime, timedelta

import sqlalchemy as sa
from flask import request
from sqlalchemy import exc as sa_exc
from typing_extensions import Unpack

from src.core import permissions
from src.core.db import db
from src.core.models.pre_regis_user import PreRegisterUser
from src.services.base import BaseService, BaseServiceError
from src.services.mail import MailService

# flake8: noqa E501


InstitutionsRoles = t.TypeVar(
    "InstitutionsRoles",
    t.Literal["OWNER"],
    t.Literal["MANAGER"],
    t.Literal["OPERATOR"],
)


class PreRegisterUserParams(t.TypedDict):
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
    def create_pre_user(cls, **kwargs: Unpack[PreRegisterUserParams]):
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
    def delete_pre_user(cls, token: str):
        """delete pre-user"""

        db.session.query(PreRegisterUser).where(
            PreRegisterUser.token == token
        ).delete()
        db.session.commit()

    @classmethod
    def get_pre_user_by_token(cls, token: str):
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

    @classmethod
    def get_user_permissions(cls, user_id: int, institution_id: int):
        stmt = sa.text(
            """
            SELECT
                permissions.name
            FROM
                users
                INNER JOIN users_institutions_roles ON users.id = users_institutions_roles.user_id
                INNER JOIN roles ON users_institutions_roles.role_id = roles.id
                INNER JOIN roles_permissions ON roles.id = roles_permissions.role_id
                INNER JOIN permissions ON roles_permissions.permission_id = permissions.id
            WHERE
                users.id = :user_id AND users_institutions_roles.institution_id = :institution_id
            """
        )
        result = db.session.scalars(
            stmt, {"user_id": user_id, "institution_id": institution_id}
        ).all()

        return result

    @classmethod
    def add_institution_role(
        cls, role: InstitutionsRoles, user_id: int, institution_id: int
    ) -> bool:
        _role = permissions.RoleEnum[role].value
        stmt = sa.text(
            """
            INSERT INTO users_institutions_roles (user_id, institution_id, role_id)
            VALUES (:user_id, :institution_id, (SELECT id FROM roles WHERE name = :role))
            """
        )
        try:
            db.session.execute(
                stmt,
                {
                    "user_id": user_id,
                    "institution_id": institution_id,
                    "role": _role,
                },
            )
            db.session.commit()
        except sa_exc.SQLAlchemyError as e:
            print(e)
            return False

        return True

    @classmethod
    def user_is_site_admin(cls, user_id: int):
        stmt = sa.text("SELECT * FROM site_admins WHERE user_id = :user_id")
        result = db.session.scalars(stmt, {"user_id": user_id}).first()

        return result is not None

    @classmethod
    def get_site_admin_permissions(cls, user_id: int):
        stmt = sa.text(
            """
            SELECT
                permissions.name
            FROM
                users
                INNER JOIN site_admins ON users.id = site_admins.user_id
                INNER JOIN roles ON site_admins.role_id = roles.id
                INNER JOIN roles_permissions ON roles.id = roles_permissions.role_id
                INNER JOIN permissions ON roles_permissions.permission_id = permissions.id
            WHERE
                users.id = :user_id
            """
        )
        result = db.session.scalars(stmt, {"user_id": user_id}).all()

        return result
