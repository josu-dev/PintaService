import flask

from src.core import enums
from src.services.auth import AuthService
from src.services.institution import InstitutionService
from src.services.request import RequestService
from src.services.service import ServiceService
from src.services.user import UserService
from src.utils import funcs, status
from src.web.controllers.api import base
from src.web.forms import api as api_forms

bp = flask.Blueprint("root", __name__)


@bp.post("/auth")
@base.validation(api_forms.AuthForm)
def auth_post(body: api_forms.AuthFormValues):
    user = UserService.validate_email_password(body["email"], body["password"])
    if user is None:
        return base.API_BAD_REQUEST_RESPONSE

    access_token = base.create_access_token(user.id)
    response = (
        {
            "token": access_token,
        },
        status.HTTP_200_OK,
    )
    return response


@bp.get("/institutions")
@base.validation(api_forms.PaginationForm, method="GET")
def institutions_get(args: api_forms.PaginationFormValues):
    page = args["page"]
    per_page = args["per_page"] or 1

    try:
        (
            raw_institutions,
            total,
        ) = InstitutionService.get_institutions(page=page, per_page=per_page)
    except InstitutionService.InstitutionServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    institutions = [
        inst.asdict(
            ("id", "created_at", "updated_at", "keywords"),
            exclude=True,
        )
        for inst in raw_institutions
    ]

    response = {
        "data": institutions,
        "page": page,
        "per_page": per_page,
        "total": total,
    }

    return response


@bp.get("/service_institution/<int:service_id>")
@base.validation(method="GET")
def institutions_id_get(service_id: int):
    institution_id = ServiceService.get_institution_of(service_id)
    if institution_id is None:
        return base.API_BAD_REQUEST_RESPONSE

    institution = InstitutionService.get_institution(institution_id)  # type: ignore # noqa: E501
    service = ServiceService.get_service(service_id)
    if institution is None or service is None:
        return base.API_BAD_REQUEST_RESPONSE

    response = {
        "data": {
            "service": {
                "name": service.name,
                "description": service.description,
                "laboratory": service.laboratory,
                "keywords": service.keywords,
                "enabled": service.enabled,
            },
            "institution": {
                "name": institution.name,
                "information": institution.information,
                "address": institution.address,
                "web": institution.web,
                "keywords": institution.keywords,
                "location": institution.location,
                "enabled": institution.enabled,
                "email": institution.email,
                "days_and_opening_hours": institution.days_and_opening_hours,  # noqa: E501
            },
        }
    }

    return response


@bp.get("/me/profile")
@base.validation(method="GET", require_auth=True)
def me_profile_get():
    user_id = base.user_id_from_access_token()
    user = UserService.get_by_id(user_id)
    if user is None:
        return base.API_BAD_REQUEST_RESPONSE

    response = {
        "user": user.username,
        "email": user.email,
        "document_type": user.document_type.value,
        "document_number": user.document_number,
        "gender": user.gender.value,
        "gender_other": user.gender_other,
        "address": user.address,
        "phone": user.phone,
    }

    return response


@bp.get("/me/requests")
@base.validation(api_forms.MeRequestsForm, method="GET", require_auth=True)
def me_requests_get(args: api_forms.MeRequestsFormValues):
    user_id = base.user_id_from_access_token()
    if not UserService.exist_user(user_id):
        return base.API_BAD_REQUEST_RESPONSE

    page = args["page"]
    per_page = args["per_page"] or flask.g.site_config.page_size
    raw_status = args["status"]
    status = (
        None
        if raw_status is None
        else [
            rstatus
            for rstatus in enums.RequestStatus
            if rstatus.value == raw_status
        ][0]
    )

    try:
        raw_requests, total = RequestService.get_requests_by_user(
            user_id,
            page=page,
            per_page=per_page,
            status=status,
            order=args["order"],
        )
    except RequestService.RequestServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    requests = [
        {
            "id": req.id,
            "title": req.title,
            "creation_date": funcs.date_as_yyyy_mm_dd(req.created_at),
            "close_date": (
                funcs.date_as_yyyy_mm_dd(req.closed_at)
                if req.closed_at
                else ""
            ),
            "status": req.status.value,
            "description": req.description,
        }
        for req in raw_requests
    ]

    response = {
        "data": requests,
        "page": page,
        "per_page": per_page,
        "total": total,
    }

    return response


@bp.get("/me/requests/<int:request_id>")
@base.validation(method="GET", require_auth=True)
def me_requests_id_get(request_id: int):
    user_id = base.user_id_from_access_token()
    if not UserService.exist_user(user_id):
        return base.API_BAD_REQUEST_RESPONSE

    try:
        request = RequestService.get_request(request_id)
    except RequestService.RequestServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    if request is None or request.user_id != user_id:
        return base.API_UNAUTHORIZED_RESPONSE

    response = {
        "id": request.id,
        "title": request.title,
        "description": request.description,
        "status": request.status.value,
        "creation_date": funcs.date_as_yyyy_mm_dd(request.created_at),
        "close_date": (
            funcs.date_as_yyyy_mm_dd(request.closed_at)
            if request.closed_at
            else ""
        ),
        "user_id": request.user_id,
        "service_id": request.service_id,
    }

    return response


@bp.post("/me/requests")
@base.validation(api_forms.ServiceRequestForm, require_auth=True)
def me_requests_post(body: api_forms.ServiceRequestFormValues):
    user_id = base.user_id_from_access_token()
    if not UserService.exist_user(user_id):
        return base.API_BAD_REQUEST_RESPONSE

    service_id = body["service_id"]
    title = body["title"]
    description = body["description"]

    try:
        service = RequestService.create_request(
            user_id,
            service_id,
            title=title,
            description=description,
            status=enums.RequestStatus.IN_PROCESS,
        )
    except RequestService.RequestServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    response = {
        "id": service.id,
        "title": service.title,
        "creation_date": funcs.date_as_yyyy_mm_dd(service.created_at),
        "close_date": "",
        "status": service.status.value,
        "description": service.description,
    }

    return response, status.HTTP_201_CREATED


@bp.get("/me/requests/<int:request_id>/notes")
@base.validation(
    api_forms.PaginationForm, method="GET", require_auth=True, debug=True
)
def me_requests_id_notes_get(
    request_id: int, args: api_forms.PaginationFormValues
):
    user_id = base.user_id_from_access_token()
    if not UserService.exist_user(user_id):
        return base.API_BAD_REQUEST_RESPONSE

    try:
        request = RequestService.get_request(request_id)
    except RequestService.RequestServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    if request is None:
        return base.API_BAD_REQUEST_RESPONSE

    if request.user_id != user_id:
        return base.API_UNAUTHORIZED_RESPONSE

    page = args["page"]
    per_page = args["per_page"] or flask.g.site_config.page_size
    try:
        raw_notes, total = RequestService.get_requests_notes_with_users(
            request_id, page=page, per_page=per_page
        )
    except RequestService.RequestServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    notes = [
        {
            "note": {
                "id": note.id,
                "text": note.note,
                "creation_date": funcs.date_as_yyyy_mm_dd(note.created_at),
            },
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
            },
        }
        for note, user in raw_notes
    ]

    response = {
        "data": notes,
        "page": page,
        "per_page": per_page,
        "total": total,
    }
    print(response)

    return response


@bp.post("/me/requests/<int:request_id>/notes")
@base.validation(api_forms.RequestNoteForm, require_auth=True)
def me_requests_id_notes_post(
    body: api_forms.RequestNoteFormValues, request_id: int
):
    user_id = base.user_id_from_access_token()
    if not UserService.exist_user(user_id):
        return base.API_BAD_REQUEST_RESPONSE

    text = body["text"]
    try:
        note = RequestService.create_note(request_id, user_id, text)
    except RequestService.RequestServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    response = {
        "id": note.id,
        "text": note.note,
        "creation_date": funcs.date_as_yyyy_mm_dd(note.created_at),
    }

    return response, status.HTTP_201_CREATED


@bp.get("/services/search")
@base.validation(api_forms.ServiceSearchForm, "GET")
def services_search_get(args: api_forms.ServiceSearchFormValues):
    q = args["q"]
    service_type_value = args["type"]
    page = args["page"]
    per_page = args["per_page"] or flask.g.site_config.page_size

    service_type = None
    if service_type_value:
        if service_type_value == enums.ServiceTypes.ANALYSIS.value:
            service_type = enums.ServiceTypes.ANALYSIS
        elif service_type_value == enums.ServiceTypes.CONSULTANCY.value:
            service_type = enums.ServiceTypes.CONSULTANCY
        elif service_type_value == enums.ServiceTypes.DEVELOPMENT.value:
            service_type = enums.ServiceTypes.DEVELOPMENT

    try:
        raw_services, total = ServiceService.search_services(
            q, service_type, page, per_page
        )
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    services = [
        {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "laboratory": service.laboratory,
            "keywords": service.keywords,
            "enabled": service.enabled,
            "service_type": service.service_type.value,
        }
        for service in raw_services
    ]

    response = {
        "data": services,
        "page": page,
        "per_page": per_page,
        "total": total,
    }

    return response


@bp.get("/services/<int:service_id>")
@base.validation(method="GET", require_auth=True)
def services_id_get(service_id: int):
    try:
        service = ServiceService.get_service(service_id)
    except ServiceService.ServiceServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    if service is None:
        return base.API_BAD_REQUEST_RESPONSE

    response = service.asdict(
        ("name", "description", "laboratory", "keywords", "enabled"),
    )

    return response


@bp.get("/services_types")
@base.validation(method="GET", require_auth=True)
def services_types_get():
    response = {
        "data": [service_type.value for service_type in enums.ServiceTypes]
    }

    return response


@bp.get("/stats/requests_per_status")
@base.validation(method="GET", require_auth=True, debug=True)
def stats_requests_per_status_get():
    user_id = base.user_id_from_access_token()
    user_is_site_admin = AuthService.user_is_site_admin(user_id)
    user_institutions = InstitutionService.get_institutions_owned_by_user(
        user_id
    )
    if not user_is_site_admin and len(user_institutions) == 0:
        return base.API_UNAUTHORIZED_RESPONSE

    owner_id = None if user_is_site_admin else user_id
    res = RequestService.get_requests_count_per_status(owner_id)

    for statusEnum in enums.RequestStatus:
        if statusEnum not in [status for status, _ in res]:
            res.append(
                (statusEnum, 0)  # pyright: ignore[reportGeneralTypeIssues]
            )

    response = {
        "data": [
            {
                "status": status.value,
                "count": count,
            }
            for status, count in res
        ]
    }

    return response


@bp.get("/stats/most_requested_services")
@base.validation(method="GET", require_auth=True)
def stats_most_requested_services_get():
    user_id = base.user_id_from_access_token()
    user_is_site_admin = AuthService.user_is_site_admin(user_id)
    user_institutions = InstitutionService.get_institutions_owned_by_user(
        user_id
    )
    if not user_is_site_admin and len(user_institutions) == 0:
        return base.API_UNAUTHORIZED_RESPONSE

    services, _ = ServiceService.get_most_requested_services(1, 10)

    response = {
        "data": [
            {
                "service": {
                    "id": service.id,
                    "name": service.name,
                    "description": service.description,
                    "laboratory": service.laboratory,
                    "keywords": service.keywords,
                    "enabled": service.enabled,
                },
                "total_requests": requests_count,
            }
            for service, requests_count in services
        ]
    }

    return response


@bp.get("/stats/most_efficient_institutions")
@base.validation(method="GET", require_auth=True)
def stats_most_efficient_institutions_get():
    user_id = base.user_id_from_access_token()
    user_is_site_admin = AuthService.user_is_site_admin(user_id)
    user_institutions = InstitutionService.get_institutions_owned_by_user(
        user_id
    )
    if not user_is_site_admin and len(user_institutions) == 0:
        return base.API_UNAUTHORIZED_RESPONSE

    institutions = InstitutionService.get_most_efficient_institutions()

    response = {
        "data": [
            {
                "institution": {
                    "id": institution.id,
                    "name": institution.name,
                    "keywords": institution.keywords,
                    "enabled": institution.enabled,
                },
                "avg_resolution_time": avg_resolution_time.total_seconds(),
            }
            for institution, avg_resolution_time in institutions
        ]
    }

    return response


@bp.get("/me/rol/site_admin")
@base.validation(method="GET", require_auth=True)
def me_rol_site_admin_get():
    user_id = base.user_id_from_access_token()
    is_site_admin = AuthService.user_is_site_admin(user_id)

    response = {
        "data": {
            "is_site_admin": is_site_admin,
        },
    }

    return response


@bp.get("/me/rol/institution_owner")
@base.validation(method="GET", require_auth=True)
def me_rol_institution_owner():
    user_id = base.user_id_from_access_token()
    is_institution_owner = InstitutionService.get_institutions_owned_by_user(
        user_id
    )

    response = {
        "data": {
            "is_institution_owner": len(is_institution_owner) > 0,
        },
    }

    return response


@bp.get("/enabled/institutions")
@base.validation(api_forms.PaginationForm, method="GET")
def enabled_institutions_get(args: api_forms.PaginationFormValues):
    page = args["page"]
    per_page = args["per_page"] or 1

    try:
        (
            raw_institutions,
            total,
        ) = InstitutionService.get_enabled_institutions(
            page=page, per_page=per_page
        )
    except InstitutionService.InstitutionServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    institutions = [
        inst.asdict(("id", "name", "information", "email"))
        for inst in raw_institutions
    ]

    response = {
        "data": institutions,
        "page": page,
        "per_page": per_page,
        "total": total,
    }

    return response


@bp.get("/enabled/institutions/<int:institution_id>/services")
@base.validation(api_forms.PaginationForm, method="GET")
def enabled_institutions_id_services_get(
    institution_id: int, args: api_forms.PaginationFormValues
):
    page = args["page"]
    per_page = args["per_page"] or 1

    try:
        (
            raw_services,
            total,
        ) = ServiceService.get_enabled_institution_services(
            institution_id=institution_id, page=page, per_page=per_page
        )
    except InstitutionService.InstitutionServiceError:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    services = [
        {
            "id": service.id,
            "institution_id": service.institution_id,
            "name": service.name,
            "description": service.description,
            "laboratory": service.laboratory,
            "keywords": service.keywords,
            "enabled": service.enabled,
            "service_type": service.service_type.value,
        }
        for service in raw_services
    ]

    response = {
        "data": services,
        "page": page,
        "per_page": per_page,
        "total": total,
    }

    return response
