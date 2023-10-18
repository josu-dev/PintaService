import typing as t

from flask import Blueprint

from src.services.user import UserService
from src.web.controllers.api import base
from src.web.forms import api as api_forms

bp = Blueprint("root", __name__)


@bp.post("/auth")
@base.validation(api_forms.AuthForm)
def auth_post(body: api_forms.AuthFormValues):
    user = UserService.validate_email_password(body["email"], body["password"])
    if not user:
        return {"result": "fail"}

    return {"result": "success"}


# TODO: remove this mock
def get_institutions(offset: int, limit: int):
    return (
        {
            "name": "Institución #1",
            "information": "Información adicional",
            "address": "Calle 50 N° 1234",
            "location": "latitude, longitude",
            "web": "www.institucion1.com",
            "days_and_opening_hours": "Lunes a viernes de 8 a 18hs",
            "email": "info@institution.com",
            "enabled": False,
        },
    )


@bp.get("/institutions")
@base.validation(api_forms.PaginationForm, "GET", content_type=False)
def institutions_get(args: api_forms.PaginationFormValues):
    page = args["page"]
    per_page = args["per_page"]
    offset = (page - 1) * per_page
    try:
        # TODO: change this to a real implementation
        institutions = get_institutions(offset, per_page)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    total = 80
    return {
        "data": institutions,
        "page": page,
        "per_page": per_page,
        "total": total,
    }


@bp.get("/me/profile")
@base.validation(auth_required=True, content_type=False)
def me_profile_get(user_id: int):
    user = UserService.get_user(user_id)
    if user is None:
        return base.API_BAD_REQUEST_RESPONSE

    response = user.asdict(
        (
            "document_type",
            "gender",
            "firstname",
            "lastname",
            "password",
            "is_active",
            "created_at",
            "updated_at",
            "id",
        ),
        True,
    )
    response["document_type"] = user.document_type.value
    response["gender"] = user.gender.value
    return response


# TODO: remove this mock
def get_paginations(offset: int, limit: int):
    return (
        {
            "title": "a title",
            "creation_date": "2023-10-10",
            "close_date": "2023-12-11",
            "status": "created",
            "description": "a long description",
        },
    )


@bp.get("/me/requests")
@base.validation(
    api_forms.PaginationForm, "GET", auth_required=True, content_type=False
)
def me_requests_get(args: api_forms.PaginationFormValues, user_id: int):
    user = UserService.get_user(user_id)
    if user is None:
        return base.API_BAD_REQUEST_RESPONSE

    page = args["page"]
    per_page = args["per_page"]
    offset = (page - 1) * per_page

    try:
        # TODO: change this to a real implementation
        paginations = get_paginations(offset, per_page)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    total = 80
    return {
        "data": paginations,
        "page": page,
        "per_page": per_page,
        "total": total,
    }


def set_service(title: str, description: str):
    return {
        "title": title,
        "creation_date": "2023-10-10",
        "close_date": "2023-12-11",
        "status": "created",
        "description": description,
    }


@bp.post("/me/requests")
@base.validation(api_forms.ServiceForm, auth_required=True, content_type=False)
def me_requests_post(body: api_forms.ServiceFormValues, user_id: int):
    user = UserService.get_user(user_id)
    if user is None:
        return base.API_BAD_REQUEST_RESPONSE

    title = body["title"]
    description = body["description"]

    try:
        # TODO: change this to a real implementation
        service = set_service(title, description)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    return service


def get_requests_id(request_id: int):
    requests = [
        {
            "title": "a title 1",
            "creation_date": "2023-10-10",
            "close_date": "2023-12-11",
            "status": "created",
            "description": "a long description",
        },
        {
            "title": "a title 2",
            "creation_date": "2023-10-10",
            "close_date": "2023-12-11",
            "status": "created",
            "description": "a long description",
        },
        {
            "title": "a title 3",
            "creation_date": "2023-10-10",
            "close_date": "2023-12-11",
            "status": "created",
            "description": "a long description",
        },
    ]
    return requests[request_id]


@bp.get("/me/requests/<int:request_id>")
@base.validation(auth_required=True, content_type=False)
def me_requests_id_get(request_id: int, user_id: int):
    user = UserService.get_user(user_id)
    if user is None:
        return base.API_BAD_REQUEST_RESPONSE

    try:
        # TODO: change this to a real implementation
        requests = get_requests_id(request_id)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    return requests


def set_note_service(text: str, request_id: int):
    return {"id": request_id, "text": text}


@bp.post("/me/requests/<int:request_id>/notes")
@base.validation(api_forms.TextForm, auth_required=True, content_type=False)
def me_requests_id_notes_post(
    body: api_forms.TextFormValues, request_id: int, user_id: int
):
    user = UserService.get_user(user_id)
    if user is None:
        return base.API_BAD_REQUEST_RESPONSE

    text = body["text"]
    try:
        # TODO: change this to a real implementation
        note = set_note_service(text, request_id)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    return note


def services_search(q: str, type: str = ""):
    requests = [
        {
            "name": "name",
            "description": "a descriptions",
            "laboratory": "laboratory name",
            "keywords": "a list of keywords",
            "enabled": False,
        },
        {
            "name": "service",
            "description": "a descriptionss",
            "laboratory": "laboratorynames",
            "keywords": "a list of keywords",
            "enabled": False,
        },
        {
            "name": "service name",
            "description": "name",
            "laboratory": "laboratory name",
            "keywords": "a list of keywords",
            "enabled": False,
        },
    ]
    print(str(q).lower(), flush=True)
    matching_requests: t.List[t.Dict[str, t.Any]] = []
    for request in requests:
        for value in request.items():
            if str(q).lower() in str(value[1]).lower():
                matching_requests.append((request))

    return matching_requests


@bp.get("/services/search")
@base.validation(api_forms.ServiceSearchForm, "GET", content_type=False)
def services_search_get(args: api_forms.ServiceSearchFormValues):
    q = args["q"]
    type = args["type"]
    page = args["page"]
    per_page = args["per_page"]
    try:
        # TODO: change this to a real implementation
        service = services_search(q, type)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    total = 25
    return {
        "data": service,
        "page": page,
        "per_page": per_page,
        "total": total,
    }


def get_service_id(service_id: int):
    services = [
        {
            "name": "service name 1",
            "description": "a description",
            "laboratory": "laboratory name",
            "keywords": "a list of keywords",
            "enabled": False,
        },
        {
            "name": "service name 2",
            "description": "a description",
            "laboratory": "laboratory name",
            "keywords": "a list of keywords",
            "enabled": False,
        },
        {
            "name": "service name 3",
            "description": "a description",
            "laboratory": "laboratory name",
            "keywords": "a list of keywords",
            "enabled": False,
        },
    ]
    return services[service_id]


@bp.get("/services/<int:service_id>")
@base.validation(content_type=False)
def service_id_get(service_id: int):
    try:
        # TODO: change this to a real implementation
        service = get_service_id(service_id)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    return service


def get_service_types():
    return ["Análisis", "Consultoría", "Desarrollo"]


@bp.get("/services-types")
@base.validation(content_type=False)
def service_types_get():
    try:
        # TODO: change this to a real implementation
        service_type = get_service_types()
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    return {"data": service_type}
