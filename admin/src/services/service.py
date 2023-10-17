import typing as t

import sqlalchemy as sa
import typing_extensions as te

from src.core.db import db
from src.core.enums import ServiceType
from src.core.models.institution import Institution
from src.core.models.institution_service import InstitutionService
from src.core.models.service import Service
from src.services.base import BaseService, BaseServiceError


class ServiceParams(t.TypedDict):
    name: str
    laboratory: str
    description: str
    keywords: str
    service_type: ServiceType


class ServiceServiceError(BaseServiceError):
    pass


class ServiceService(BaseService):
    """Service for handling services."""

    ServiceServiceError = ServiceServiceError

    @classmethod
    def get_services(cls) -> t.List[Service]:
        return db.session.query(Service).all()

    @classmethod
    def get_service(cls, service_id: int) -> t.Optional[Service]:
        return db.session.query(Service).get(service_id)

    @classmethod
    def update_service(
        cls, service_id: int, **kwargs: te.Unpack[ServiceParams]
    ):
        service = db.session.query(Service).get(service_id)
        if service:
            for key, value in kwargs.items():
                setattr(service, key, value)
            db.session.commit()
            return service
        return None

    @classmethod
    def delete_service(cls, service_id: int):
        service = db.session.query(Service).get(service_id)
        if service:
            db.session.delete(service)
            db.session.commit()

    @classmethod
    def create_service(
        cls, institution_id: int, **kwargs: te.Unpack[ServiceParams]
    ):
        """Create service in the database."""
        service = Service(**kwargs)

        institution = db.session.query(Institution).get(institution_id)

        if institution is None:
            raise ServiceServiceError("Institution not found")

        service.institutions.append(institution)

        db.session.add(service)
        db.session.commit()

    @classmethod
    def get_institution_services(cls, institution_id: int) -> t.List[Service]:
        return (
            db.session.query(Service)
            .join(
                InstitutionService,
                sa.and_(
                    Service.id == InstitutionService.service_id,
                    InstitutionService.institution_id == institution_id,
                ),
            )
            .all()
        )
