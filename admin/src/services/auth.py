import secrets
import typing as t
from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy import exc as sa_exc
from typing_extensions import Unpack

from src.core import permissions
from src.core.db import db
from src.core.enums import RegisterTypes
from src.core.models.auth import Role, UserInstitutionRole
from src.core.models.user import PreRegisterUser
from src.services.base import BaseService, BaseServiceError

# flake8: noqa E501

InstitutionsRoles = t.Literal["OWNER", "MANAGER", "OPERATOR"]


class PreRegisterUserParams(t.TypedDict):
    firstname: str
    lastname: str
    email: str


class AuthServiceError(BaseServiceError):
    pass


class AuthService(BaseService):
    """Service for handling auth.

    This service is used for handling the first step of the registration
    process and the general permissions of the users.
    """

    AuthServiceError = AuthServiceError

    @classmethod
    def get_pre_user_by_email(
        cls, email: str
    ) -> t.Union[PreRegisterUser, None]:
        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.email == email)
            .first()
        )

    @classmethod
    def create_pre_user(
        cls,
        register_type: RegisterTypes,
        **kwargs: Unpack[PreRegisterUserParams],
    ) -> PreRegisterUser:
        """Creates a pre-user.

        This method creates a pre-user that will be used for the first step of
        the registration process.

        Raises:
            AuthServiceError: If the email already exists.
        """
        if AuthService.get_pre_user_by_email(kwargs["email"]):
            raise AuthServiceError(f"{kwargs['email']} Email already exists")

        token = secrets.token_urlsafe(64)
        user = PreRegisterUser(
            **kwargs, token=token, register_type=register_type
        )
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def delete_pre_user(cls, token: str) -> bool:
        """Deletes a pre-user by token.

        Returns:
            bool: True if the pre-user exists and was deleted, False if the
                pre-user was not deleted or if the pre-user does not exist.
        """
        delete_count = (
            db.session.query(PreRegisterUser)
            .where(PreRegisterUser.token == token)
            .delete()
        )
        db.session.commit()
        return delete_count == 1

    @classmethod
    def get_pre_user_by_token(
        cls, token: str
    ) -> t.Union[PreRegisterUser, None]:
        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.token == token)
            .first()
        )

    @classmethod
    def exist_pre_user_with_email(cls, email: str) -> bool:
        return (
            db.session.query(PreRegisterUser)
            .filter(PreRegisterUser.email == email)
            .first()
            is not None
        )

    @classmethod
    def token_expired(cls, token_date: datetime) -> bool:
        """Checks if the token date is expired (more than one day)."""
        current_date = datetime.now()
        difference = current_date - token_date
        one_day = timedelta(days=1)
        return difference > one_day

    @classmethod
    def get_user_permissions(
        cls, user_id: int, institution_id: int
    ) -> t.Sequence[str]:
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
        """Adds a role to a user in an institution.

        No checks are made to see if the user already has the role.

        Returns:
            bool: True if the role was added, False otherwise.
        """
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
    def remove_institution_role(
        cls, user_id: int, institution_id: int, role: InstitutionsRoles
    ) -> bool:
        """Removes a role from a user in an institution.

        Returns:
            bool: True if the role was removed, False if the role was not
                removed or if the user did not have the role.
        """
        role_name = permissions.RoleEnum[role].value
        try:
            delete_count = (
                db.session.query(UserInstitutionRole)
                .filter(
                    UserInstitutionRole.user_id == user_id,
                    UserInstitutionRole.institution_id == institution_id,
                    UserInstitutionRole.role_id
                    == db.session.query(Role.id)
                    .filter(Role.name == role_name)
                    .scalar_subquery(),
                )
                .delete()
            )
            db.session.commit()
        except sa_exc.SQLAlchemyError as e:
            print("error", e, flush=True)
            return False

        return delete_count == 1

    @classmethod
    def user_is_site_admin(cls, user_id: int) -> bool:
        stmt = sa.text("SELECT * FROM site_admins WHERE user_id = :user_id")
        result = db.session.scalars(stmt, {"user_id": user_id}).first()

        return result is not None

    @classmethod
    def get_site_admin_permissions(cls, user_id: int) -> t.Sequence[str]:
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
