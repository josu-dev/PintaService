import datetime
import typing as t

import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import typing_extensions as te

from src.core import enums, permissions
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
    """Service for handling institutions.

    This service is used for CRUD operations on institutions and for
    managing the users that are associated with an institution.
    """

    InstitutionServiceError = InstitutionServiceError

    @classmethod
    def get_all_institutions(cls) -> t.List[Institution]:
        institutions = db.session.query(Institution).all()

        return institutions

    @classmethod
    def get_institutions(
        cls, page: int = 1, per_page: int = 10
    ) -> t.Tuple[t.List[Institution], int]:
        query = db.session.query(Institution)
        total = query.count()
        institutions = (
            query.offset((page - 1) * per_page).limit(per_page).all()
        )

        return institutions, total

    @classmethod
    def get_enabled_institutions(
        cls, page: int = 1, per_page: int = 10
    ) -> t.Tuple[t.List[Institution], int]:
        query = db.session.query(Institution).filter(Institution.enabled)

        total = query.count()
        institutions = (
            query.offset((page - 1) * per_page).limit(per_page).all()
        )

        return institutions, total

    @classmethod
    def get_institution(
        cls, institution_id: int
    ) -> t.Union[Institution, None]:
        return db.session.query(Institution).get(institution_id)

    @classmethod
    def create_institution(
        cls, **kwargs: te.Unpack[InstitutionParams]
    ) -> Institution:
        """Create a new institution.

        Raises:
            InstitutionServiceError: If the institution could not be created.
        """
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
    ) -> t.Union[Institution, None]:
        """Update an existing institution by id.

        Returns:
            Institution: The updated institution.
            None: If the institution could not be found.
        """
        institution = db.session.query(Institution).get(institution_id)
        if institution:
            for key, value in kwargs.items():
                setattr(institution, key, value)
            db.session.commit()
            return institution

        return None

    @classmethod
    def delete_institution(cls, institution_id: int) -> bool:
        """Delete an institution by id.

        The deletion of an institution cascades to all the services, requests
        and notes associated with the institution.

        Returns:
            bool: True if the institution was deleted, False if the institution
                was not deleted or if the institution could not be found.
        """
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

    @classmethod
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
    def get_rol(cls, role_name: str) -> t.Union[Role, None]:
        role = (db.session.query(Role).filter(Role.name == role_name)).first()

        return role

    @classmethod
    def delete_institution_user(
        cls, institution_id: int, user_id: int
    ) -> bool:
        """Delete a user from an institution.

        Removes the role of the user in the institution.

        Returns:
            bool: True if the user was removed, False if the user was not
                removed or if the user did not have a role in the institution.
        """
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
        if result is None:
            return False

        return True

    @classmethod
    def get_institutions_owned_by_user(
        cls, user_id: int
    ) -> t.List[Institution]:
        institutions = (
            db.session.query(Institution)
            .join(
                UserInstitutionRole,
                sa.and_(
                    UserInstitutionRole.institution_id == Institution.id,
                    UserInstitutionRole.user_id == user_id,
                    UserInstitutionRole.role_id
                    == db.session.query(Role.id)
                    .filter(Role.name == permissions.RoleEnum.OWNER.value)
                    .scalar_subquery(),
                ),
            )
            .all()
        )

        return institutions

    @classmethod
    def get_most_efficient_institutions(
        cls,
    ) -> t.List[t.Tuple[Institution, datetime.timedelta]]:
        query = (
            db.session.query(
                Institution,
                sa.func.avg(
                    ServiceRequest.updated_at - ServiceRequest.created_at
                ).label("avg_resolution_time"),
            )
            .join(
                ServiceRequest,
                Institution.id == ServiceRequest.institution_id,
            )
            .filter(ServiceRequest.status == enums.RequestStatus.FINISHED)
            .group_by(Institution.id)
            .order_by("avg_resolution_time")
            .limit(10)
        )
        res = query.all()

        return res  # pyright: ignore[reportGeneralTypeIssues]
