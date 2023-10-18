import typing as t

import typing_extensions as te

from src.core.db import db
from src.core.enums import RequestStatus
from src.core.models.service_requests import RequestNote, ServiceRequest
from src.core.models.user import User
from src.services.base import BaseService, BaseServiceError


class RequestParams(t.TypedDict):
    title: str
    description: str
    status: RequestStatus


class RequestNoteParam(t.TypedDict):
    note: str


class RequestServiceError(BaseServiceError):
    pass


class RequestService(BaseService):
    @classmethod
    def get_request(cls, request_id: int) -> ServiceRequest:
        query = db.session.get(ServiceRequest, request_id)
        """Get request from database"""
        if query is None:
            raise RequestServiceError("Solicitud no encontrada")
        return query

    @classmethod
    def get_requests_of(
        cls, institution_id: int, page: int = 1, per_page: int = 10
    ) -> t.Tuple[t.List[ServiceRequest], int]:
        """Get requests from database"""
        requests = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.institution_id == institution_id)
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
    def update_state_request(cls, request_id: int, state: RequestStatus):
        request = (
            db.session.query(ServiceRequest)
            .filter(ServiceRequest.id == request_id)
            .first()
        )
        if request is None:
            raise RequestServiceError("Solicitud no encontrada")
        request.status = state
        db.session.add(request)
        db.session.commit()

    @classmethod
    def create_request(
        cls,
        user_id: int,
        institution_id: int,
        service_id: int,
        **kwargs: te.Unpack[RequestParams]
    ):
        request = ServiceRequest(
            user_id=user_id,
            institution_id=institution_id,
            service_id=service_id,
            **kwargs
        )
        db.session.add(request)
        db.session.commit()
        return request

    @classmethod
    def get_request_notes(cls, request_id: int):
        query = (
            db.session.query(RequestNote.note, User.username)
            .join(User, User.id == RequestNote.user_id)
            .filter(RequestNote.service_request_id == request_id)
            .all()
        )
        return query  # type :ignore

    @classmethod
    def create_note(cls, service_request_id: int, note: str, user_id: int):
        request = RequestNote(
            note=note, service_request_id=service_request_id, user_id=user_id
        )
        db.session.add(request)
        db.session.commit()
