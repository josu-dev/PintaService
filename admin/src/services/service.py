import typing as t

import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import typing_extensions as te

from src.core.db import db
from src.core.enums import ServiceTypes
from src.core.models.institution import Institution
from src.core.models.service import Service
from src.core.models.service_requests import RequestNote, ServiceRequest
from src.services.base import BaseService, BaseServiceError


class ServiceParams(t.TypedDict):
    name: str
    description: str
    keywords: str
    service_type: ServiceTypes
    enabled: te.NotRequired[bool]


class ServicePartialParams(t.TypedDict):
    name: te.NotRequired[str]
    description: te.NotRequired[str]
    keywords: te.NotRequired[str]
    service_type: te.NotRequired[ServiceTypes]
    laboratory: te.NotRequired[str]
    enabled: te.NotRequired[bool]


class ServiceServiceError(BaseServiceError):
    pass


class ServiceService(BaseService):
    """Service for handling institutions services.

    This service is used for CRUD operations on institutions services and for
    searching services.
    """

    ServiceServiceError = ServiceServiceError

    @classmethod
    def get_services(cls) -> t.List[Service]:
        return db.session.query(Service).all()

    @classmethod
    def get_service(cls, service_id: int) -> t.Union[Service, None]:
        return (
            db.session.query(Service).filter(Service.id == service_id).first()
        )

    @classmethod
    def create_service(
        cls, institution_id: int, **kwargs: te.Unpack[ServiceParams]
    ) -> Service:
        """Creates a service for an institution.

        Raises:
            ServiceServiceError: If the institution does not exist.
        """
        institution: t.Union[Institution, None] = db.session.query(
            Institution
        ).get(institution_id)
        if institution is None:
            raise ServiceServiceError("Institution not found")

        service = Service(
            institution_id=institution_id,
            laboratory=institution.name,
            **kwargs,
        )
        db.session.add(service)
        db.session.commit()

        return service

    @classmethod
    def update_service(
        cls, service_id: int, **kwargs: te.Unpack[ServiceParams]
    ) -> t.Union[Service, None]:
        """Updates a service.

        Returns:
            Service: The updated service.
            None: If the service does not exist.

        Raises:
            ServiceServiceError: If the service could not be updated.
        """
        service = db.session.query(Service).get(service_id)
        if service is None:
            return None

        try:
            for key, value in kwargs.items():
                setattr(service, key, value)
            db.session.commit()
            return service
        except sa_exc.SQLAlchemyError as e:
            db.session.rollback()
            raise ServiceServiceError(
                f"Could not update service '{service_id}': {e.code}"
            )

    @classmethod
    def delete_service(cls, service_id: int) -> bool:
        """Deletes a service.

        The deletion is cascaded to all service requests and notes.

        Returns:
            bool: True if the service was deleted, False if the service was not
                deleted or if the service did not exist.
        """
        # Delete using complex join are not supported by SQLAlchemy
        (
            db.session.query(RequestNote)
            .filter(
                RequestNote.id.in_(
                    sa.select(RequestNote.id).join(
                        ServiceRequest,
                        sa.and_(
                            ServiceRequest.id
                            == RequestNote.service_request_id,
                            ServiceRequest.service_id == service_id,
                        ),
                    )
                )
            )
            .delete()
        )
        (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.service_id == service_id)
            .delete()
        )
        delete_count = (
            db.session.query(Service).filter(Service.id == service_id).delete()
        )
        db.session.commit()

        return delete_count == 1

    @classmethod
    def get_institution_services(cls, institution_id: int) -> t.List[Service]:
        return (
            db.session.query(Service)
            .filter(Service.institution_id == institution_id)
            .all()
        )

    @classmethod
    def get_institution_services_paginated(
        cls, institution_id: int, page: int, per_page: int
    ) -> t.Tuple[t.List[Service], int]:
        query = db.session.query(Service).filter(
            Service.institution_id == institution_id
        )
        total = query.count()
        services = query.offset((page - 1) * per_page).limit(per_page).all()

        return services, total

    @classmethod
    def search_services(
        cls,
        q: str,
        service_type: t.Union[ServiceTypes, None],
        page: int,
        per_page: int,
    ) -> t.Tuple[t.List[Service], int]:
        """Searches services.

        The search is performed by filtering services by name, description,
        keywords, laboratory and service type.

        Args:
            q: The query string.
            service_type: The service type to filter by.
            page: The page number.
            per_page: The number of services per page.
        """
        query = db.session.query(Service)
        if q != "":
            query = query.filter(
                sa.or_(
                    Service.name.ilike(f"%{q}%"),
                    Service.description.ilike(f"%{q}%"),
                    Service.keywords.ilike(f"%{q}%"),
                    Service.laboratory.ilike(f"%{q}%"),
                )
            )

        if service_type is not None:
            query = query.filter(Service.service_type == service_type)

        total = query.count()
        services = query.offset((page - 1) * per_page).limit(per_page).all()

        return services, total
