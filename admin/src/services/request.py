import typing as t
from datetime import datetime

import typing_extensions as te

from src.core.db import db
from src.core.enums import RequestStatus, ServiceTypes
from src.core.models.service import Service
from src.core.models.service_requests import (
    RequestHistory,
    RequestNote,
    ServiceRequest,
)
from src.core.models.user import User
from src.services.base import BaseService, BaseServiceError


class RequestParams(t.TypedDict):
    title: str
    description: str
    status: RequestStatus


class FilterRequestParams(t.TypedDict):
    user_email: te.NotRequired[str]
    service_type: te.NotRequired[ServiceTypes]
    status: te.NotRequired[RequestStatus]
    start_date: te.NotRequired[str]
    end_date: te.NotRequired[str]


class RequestNoteParams(t.TypedDict):
    note: str


class RequestHistoryParams(t.TypedDict):
    status: RequestStatus
    observations: str


class RequestServiceError(BaseServiceError):
    pass


class RequestService(BaseService):
    """Service for requests of institutions services.

    This service is used for CRUD operations of service requests.
    """

    RequestServiceError = RequestServiceError

    @classmethod
    def get_request(cls, request_id: int) -> t.Union[ServiceRequest, None]:
        request = db.session.get(ServiceRequest, request_id)

        return request

    @classmethod
    def get_requests_of(
        cls,
        institution_id: int,
        service_id: int,
        page: int = 1,
        per_page: int = 10,
    ) -> t.Tuple[t.List[ServiceRequest], int]:
        requests = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.institution_id == institution_id)
            .filter(ServiceRequest.service_id == service_id)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        total: int = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.institution_id == institution_id)
            .count()
        )

        return requests, total

    @classmethod
    def get_requests_by_user(
        cls, user_id: int, page: int = 1, per_page: int = 10
    ) -> t.Tuple[t.List[ServiceRequest], int]:
        query = db.session.query(ServiceRequest).filter(
            ServiceRequest.user_id == user_id
        )

        total = query.count()
        requests = query.offset((page - 1) * per_page).limit(per_page).all()

        return requests, total

    @classmethod
    def get_requests(
        cls, page: int = 1, per_page: int = 10
    ) -> t.Tuple[t.List[ServiceRequest], int]:
        return (
            db.session.query(ServiceRequest)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all(),
            db.session.query(ServiceRequest).count(),
        )

    @classmethod
    def update_state_request(
        cls, request_id: int, **kwargs: te.Unpack[RequestHistoryParams]
    ) -> bool:
        """Update the state of a request.

        Returns:
            True if the request was updated, False otherwise.

        Raises:
            RequestServiceError: If the request is not found.
        """
        request = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.id == request_id)
            .first()
        )
        if request is None:
            raise RequestServiceError("Solicitud no encontrada")

        new_status = kwargs["status"]
        if (
            new_status is not None  # type:ignore
            and new_status != request.status.name  # type:ignore
        ):
            request.status = new_status
            cls.create_request_history(
                request_id, new_status, kwargs["observations"]
            )
            db.session.add(request)
            db.session.commit()
            return True

        return False

    @classmethod
    def create_request_history(
        cls, request_id: int, state: RequestStatus, observations: str
    ) -> RequestHistory:
        """Creates a new request history entry.

        Raises:
            RequestServiceError: If the request is not found.
        """
        request = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.id == request_id)
            .first()
        )

        if request is None:
            raise RequestServiceError("Solicitud no encontrada")

        request = RequestHistory(
            service_request_id=request_id,
            status=state,
            observations=observations,
        )
        db.session.add(request)
        db.session.commit()

        return request

    @classmethod
    def create_request(
        cls,
        user_id: int,
        service_id: int,
        **kwargs: te.Unpack[RequestParams],
    ) -> ServiceRequest:
        """Creates a new service request.

        Raises:
            RequestServiceError: If the service is not found.
        """
        service = (
            db.session.query(Service).filter(Service.id == service_id).first()
        )
        if service is None:
            raise RequestServiceError(f"Servicio {service_id} no encontrado")

        request = ServiceRequest(
            user_id=user_id,
            institution_id=service.institution_id,
            service_id=service_id,
            **kwargs,
        )
        db.session.add(request)
        db.session.commit()

        return request

    @classmethod
    def get_service_request_details(cls, service_request_id: int):
        query = (
            db.session.query(ServiceRequest, User, Service)
            .join(User, User.id == ServiceRequest.user_id)
            .join(Service, Service.id == ServiceRequest.service_id)
            .filter(ServiceRequest.id == service_request_id)
            .first()
        )

        return query

    @classmethod
    def get_request_notes(cls, request_id: int):
        query = (
            db.session.query(User.username, RequestNote.note)
            .join(User, User.id == RequestNote.user_id)
            .filter(RequestNote.service_request_id == request_id)
            .all()
        )

        return query

    @classmethod
    def create_note(
        cls, service_request_id: int, user_id: int, note: str
    ) -> RequestNote:
        """Creates a new note for a service request.

        Raises:
            RequestServiceError: If the service request is not found.
        """
        request = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.id == service_request_id)
            .first()
        )
        if request is None:
            raise RequestServiceError(
                f"Solicitud {service_request_id} no encontrada"
            )

        request = RequestNote(
            service_request_id=service_request_id, user_id=user_id, note=note
        )
        db.session.add(request)
        db.session.commit()

        return request

    @classmethod
    def get_requests_notes_of_user(cls, user_id: int) -> t.List[RequestNote]:
        return (
            db.session.query(RequestNote)
            .filter(RequestNote.user_id == user_id)
            .all()
        )

    @classmethod
    def get_requests_filter_by_service(
        cls,
        page: int,
        per_page: int,
        institution_id: int,
        service_id: int,
        **kwargs: te.Unpack[FilterRequestParams],
    ) -> t.Tuple[t.List[ServiceRequest], int]:
        query = db.session.query(ServiceRequest)
        query = query.filter(ServiceRequest.institution_id == institution_id)
        query = query.filter(ServiceRequest.service_id == service_id)
        if "user_email" in kwargs:
            query = query.join(User, User.id == ServiceRequest.user_id)
            email = kwargs["user_email"]
            query = query.filter(User.email.ilike(f"%{email}%"))

        if "status" in kwargs:
            query = query.filter(ServiceRequest.status == kwargs["status"])

        if "start_date" in kwargs and kwargs["start_date"]:
            start_date = datetime.strptime(kwargs["start_date"], "%Y-%m-%d")
            query = query.filter(ServiceRequest.created_at >= start_date)

        if "end_date" in kwargs and kwargs["end_date"]:
            end_date = datetime.strptime(kwargs["end_date"], "%Y-%m-%d")
            query = query.filter(ServiceRequest.created_at <= end_date)

        total = query.count()
        requests = query.offset((page - 1) * per_page).limit(per_page).all()

        return requests, total

    @classmethod
    def get_requests_filter_by(
        cls,
        page: int,
        per_page: int,
        **kwargs: te.Unpack[FilterRequestParams],
    ) -> t.Tuple[t.List[ServiceRequest], int]:
        query = db.session.query(ServiceRequest)
        if "user_email" in kwargs:
            query = query.join(User, User.id == ServiceRequest.user_id)
            email = kwargs["user_email"]
            query = query.filter(User.email.ilike(f"%{email}%"))

        if "status" in kwargs:
            query = query.filter(ServiceRequest.status == kwargs["status"])

        if "service_type" in kwargs:
            query = query.join(
                Service, Service.id == ServiceRequest.service_id
            )
            query = query.filter(
                Service.service_type == kwargs["service_type"]
            )

        if "start_date" in kwargs and kwargs["start_date"]:
            start_date = datetime.strptime(kwargs["start_date"], "%Y-%m-%d")
            query = query.filter(ServiceRequest.created_at >= start_date)

        if "end_date" in kwargs and kwargs["end_date"]:
            end_date = datetime.strptime(kwargs["end_date"], "%Y-%m-%d")
            query = query.filter(ServiceRequest.created_at <= end_date)

        total = query.count()
        requests = query.offset((page - 1) * per_page).limit(per_page).all()

        return requests, total

    @classmethod
    def get_request_history(cls, request_id: int) -> t.List[RequestHistory]:
        return (
            db.session.query(RequestHistory)
            .filter(RequestHistory.service_request_id == request_id)
            .all()
        )
