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
    laboratory: str
    description: str
    keywords: str
    service_type: ServiceTypes


class ServiceServiceError(BaseServiceError):
    pass


class ServiceService(BaseService):
    ServiceServiceError = ServiceServiceError

    @classmethod
    def get_services(cls) -> t.List[Service]:
        return db.session.query(Service).all()

    @classmethod
    def get_service(cls, service_id: int) -> t.Union[Service, None]:
        return db.session.query(Service).get(service_id)

    @classmethod
    def create_service(
        cls, institution_id: int, **kwargs: te.Unpack[ServiceParams]
    ) -> Service:
        institution = db.session.query(Institution).get(institution_id)
        if institution is None:
            raise ServiceServiceError("Institution not found")

        service = Service(institution_id=institution_id, **kwargs)

        db.session.add(service)
        db.session.commit()
        return service

    @classmethod
    def update_service(
        cls, service_id: int, **kwargs: te.Unpack[ServiceParams]
    ) -> t.Union[Service, None]:
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
