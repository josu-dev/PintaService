import typing as t

import sqlalchemy as sa
import typing_extensions as te

from src.core.db import db
from src.core.models.auth import UserInstitutionRole
from src.core.models.institution import Institution
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
    def create_institution(cls, **kwargs: te.Unpack[InstitutionParams]):
        """Create a new institution in the database."""
        institution = Institution(**kwargs)
        db.session.add(institution)
        db.session.commit()

    @classmethod
    def update_institution(
        cls, institution_id: int, **kwargs: te.Unpack[InstitutionParams]
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
    def delete_institution(cls, institution_id: int):
        """Delete an institution from the database."""
        institution = db.session.query(Institution).get(institution_id)
        if institution:
            db.session.delete(institution)
            db.session.commit()

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
