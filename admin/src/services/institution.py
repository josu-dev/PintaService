import typing as t

import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import typing_extensions as te

from src.core import permissions
from src.core.db import db
from src.core.models.auth import Role, UserInstitutionRole
from src.core.models.institution import Institution
from src.core.models.user import User
from src.services.base import BaseService, BaseServiceError


class InstitutionParams(t.TypedDict):
    name: str
    information: str
    address: str
    location: str
    web: str
    keywords: str
    email: str
    days_and_opening_hours: str


class InstitutionPartialParams(t.TypedDict):
    name: te.NotRequired[str]
    information: te.NotRequired[str]
    address: te.NotRequired[str]
    location: te.NotRequired[str]
    web: te.NotRequired[str]
    keywords: te.NotRequired[str]
    email: te.NotRequired[str]
    days_and_opening_hours: te.NotRequired[str]
    enabled: te.NotRequired[bool]


class InstitutionServiceError(BaseServiceError):
    pass


class InstitutionService(BaseService):
    """Service for handling institutions."""

    InstitutionServiceError = InstitutionServiceError

    @classmethod
    def get_institutions(cls) -> t.List[Institution]:
        """Get all institutions from the database."""
        return db.session.query(Institution).all()

    @classmethod
    def get_institution(cls, institution_id: int) -> t.Optional[Institution]:
        """Get an institution by its ID."""
        return db.session.query(Institution).get(institution_id)

    @classmethod
    def create_institution(
        cls, **kwargs: te.Unpack[InstitutionParams]
    ) -> Institution:
        institution = Institution(**kwargs)
        try:
            db.session.add(institution)
            db.session.commit()
            return institution
        except sa_exc.SQLAlchemyError as e:
            db.session.rollback()
            raise InstitutionServiceError(
                f"Could not create institution: {e.code}"
            )

    @classmethod
    def update_institution(
        cls, institution_id: int, **kwargs: te.Unpack[InstitutionPartialParams]
    ):
        """Update an existing institution in the database."""
        institution = db.session.query(Institution).get(institution_id)
        if institution:
            for key, value in kwargs.items():
                setattr(institution, key, value)
            db.session.commit()
            return institution
        return None

    @classmethod
    def delete_institution(cls, institution_id: int) -> bool:
        """Delete an institution from the database."""
        delete_count = (
            db.session.query(Institution)
            .filter(Institution.id == institution_id)
            .delete()
        )
        db.session.commit()
        return delete_count == 1

    @classmethod
    def get_user_institutions(cls, user_id: int) -> t.List[Institution]:
        """Get all institutions from the database."""
        result = (
            db.session.query(Institution)
            .join(
                UserInstitutionRole,
                sa.and_(
                    UserInstitutionRole.institution_id == Institution.id,
                    UserInstitutionRole.user_id == user_id,
                ),
            )
            .all()
        )
        return result

    @classmethod
    def user_has_institutions(cls, user_id: int) -> bool:
        """Check if a user has institutions."""
        return (
            db.session.query(Institution.id)
            .join(
                UserInstitutionRole,
                sa.and_(
                    UserInstitutionRole.institution_id == Institution.id,
                    UserInstitutionRole.user_id == user_id,
                ),
            )
            .first()
            is not None
        )

    @classmethod
    def get_institution_owner(cls, institution_id: int) -> t.Union[User, None]:
        res = (
            db.session.query(User)
            .join(
                UserInstitutionRole,
                sa.and_(
                    User.id == UserInstitutionRole.user_id,
                    UserInstitutionRole.institution_id == institution_id,
                    UserInstitutionRole.role_id
                    == db.session.query(Role.id)
                    .filter(Role.name == permissions.RoleEnum.OWNER.value)
                    .scalar_subquery(),
                ),
            )
            .first()
        )
        return res
