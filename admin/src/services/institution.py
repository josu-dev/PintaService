import typing as t

import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import typing_extensions as te

from src.core import permissions
from src.core.db import db
from src.core.models.auth import Role, UserInstitutionRole
from src.core.models.institution import Institution
from src.core.models.service import Service
from src.core.models.service_requests import RequestNote, ServiceRequest
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
    def get_institutions(
        cls, page: int = 1, per_page: int = 10
    ) -> t.Tuple[t.List[Institution], int]:
        """Get institutions from the database."""
        institutions = (
            db.session.query(Institution)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        total = db.session.query(Institution).count()
        return institutions, total

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
        (
            db.session.query(RequestNote)
            .filter(
                RequestNote.id.in_(
                    sa.select(RequestNote.id)
                    .join(
                        ServiceRequest,
                        sa.and_(
                            ServiceRequest.id == RequestNote.service_request_id
                        ),
                    )
                    .join(
                        Service,
                        sa.and_(
                            Service.id == ServiceRequest.service_id,
                            Service.institution_id == institution_id,
                        ),
                    )
                )
            )
            .delete()
        )
        (
            db.session.query(ServiceRequest)
            .filter(
                ServiceRequest.id.in_(
                    sa.select(ServiceRequest.id).join(
                        Service,
                        sa.and_(
                            Service.id == ServiceRequest.service_id,
                            Service.institution_id == institution_id,
                        ),
                    )
                )
            )
            .delete()
        )
        (
            db.session.query(Service)
            .filter(Service.institution_id == institution_id)
            .delete()
        )
        (
            db.session.query(UserInstitutionRole)
            .filter(UserInstitutionRole.institution_id == institution_id)
            .delete()
        )
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
    def get_institution_owners(cls, institution_id: int) -> t.List[User]:
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
            .all()
        )
        return res

    def get_institution_users(
        cls, institution_id: int, page: int, per_page: int
    ):
        query = (
            db.session.query(User, Role)
            .join(
                UserInstitutionRole,
                sa.and_(
                    User.id == UserInstitutionRole.user_id,
                    UserInstitutionRole.institution_id == institution_id,
                ),
            )
            .filter(
                UserInstitutionRole.role_id.in_(
                    db.session.query(Role.id)
                    .filter(Role.name != permissions.RoleEnum.OWNER.value)
                    .scalar_subquery(),
                )
            )
            .filter(UserInstitutionRole.role_id == Role.id)
            .order_by(User.id)
        )
        total: int = query.count()
        users = query.offset((page - 1) * per_page).limit(per_page).all()
        return users, total

    @classmethod
    def update_institution_role(
        cls, institution_id: int, user_id: int, role_id: int
    ) -> bool:
        user_institution_role = (
            db.session.query(UserInstitutionRole)
            .filter(
                UserInstitutionRole.institution_id == institution_id,
                UserInstitutionRole.user_id == user_id,
            )
            .first()
        )
        if user_institution_role is None:
            return False

        user_institution_role.user_id = user_id
        user_institution_role.institution_id = institution_id
        user_institution_role.role_id = role_id
        db.session.commit()
        return True

    @classmethod
    def get_rol(cls, name_role: str) -> t.Union[Role, None]:
        role = (db.session.query(Role).filter(Role.name == name_role)).first()
        return role

    @classmethod
    def delete_institution_user(
        cls, institution_id: int, user_id: int
    ) -> bool:
        user_institution = (
            db.session.query(UserInstitutionRole)
            .filter(
                UserInstitutionRole.institution_id == institution_id,
                UserInstitutionRole.user_id == user_id,
            )
            .first()
        )
        if user_institution is None:
            return False

        db.session.delete(user_institution)
        db.session.commit()
        return True

    @classmethod
    def institution_has_user(cls, user_id: int, institution_id: int) -> bool:
        result = (
            db.session.query(UserInstitutionRole)
            .filter(
                UserInstitutionRole.institution_id == institution_id,
                UserInstitutionRole.user_id == user_id,
            )
            .first()
        )
        if result:
            return True
        return False
