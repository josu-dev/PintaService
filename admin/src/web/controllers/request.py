from flask import Blueprint, g, redirect, render_template, request

from src.core.enums import RequestStatus
from src.services.request import RequestService
from src.web.controllers import _helpers as h
from src.web.forms.request import RequestForm, RequestNoteForm

bp = Blueprint("requests", __name__)


@bp.get("/")
@h.authenticated_route(module="service_request", permissions=("index", "show"))
def requests_get(institution_id: int, service_id: int):
    """Get requests from database filtered if is neccesary"""

    site_config_pages = g.site_config.page_size
    page = request.values.get("page", 1, type=int)
    per_page = request.values.get("per_page", site_config_pages, type=int)

    service_type = request.args.get("service_type")
    status = request.args.get("status")
    user_email = request.args.get("user_email")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if user_email == "" or user_email is None:
        user_email = None
    if status == "" or status is None:
        status = None
    if service_type == "" or service_type is None:
        service_type = None

    (
        requests,  # type:ignore
        total,  # type:ignore
    ) = RequestService.get_requests_filter_by(  # type:ignore
        per_page=per_page,
        page=page,
        service_type=service_type,  # type:ignore
        status=status,  # type:ignore
        user_email=user_email,  # type:ignore
        start_date=start_date,  # type:ignore
        end_date=end_date,  # type:ignore
    )

    statuses = [status.value for status in RequestStatus]
    return render_template(
        "institutions/[id]/services/[id]/requests/index.html",
        requests=requests,
        institution_id=institution_id,
        service_id=service_id,
        page=page,
        per_page=per_page,
        total=total,
        statuses=statuses,
        user_email=user_email,
        service_type=service_type,
        status=status,
        start_date=start_date,
        end_date=end_date,
    )


@bp.get("/new")
@h.authenticated_route(module="service_request", permissions=("create",))
def requests_new_get(institution_id: int, service_id: int):
    form = RequestForm()

    return render_template(
        "institutions/[id]/services/[id]/requests/new.html", form=form
    )


@bp.post("/new")
@h.authenticated_route(
    module="service_request", permissions=("create",)
)  # Only for devs this is not the final permission
def request_new_post(institution_id: int, service_id: int):
    form = RequestForm()
    if form.validate_on_submit():
        RequestService.create_request(
            service_id=service_id,
            user_id=g.user.id,
            **form.values(),
        )
        return redirect(
            f"/institutions/{institution_id}/services/{service_id}/requests"
        )
    return render_template(
        "institutions/[id]/services/[id]/requests/new.html", form=form
    )


@bp.post("/<int:request_id>/edit")
@h.authenticated_route(module="service_request", permissions=("update",))
def request_id_edit_post(
    institution_id: int, service_id: int, request_id: int
):
    """Update a request."""
    requestElement = RequestService.get_request(request_id)

    if not requestElement:
        h.flash_error("Solicitud no encontrada.")
        return redirect(
            f"/institutions/{institution_id}/services/{service_id}/requests"
        )

    selected_status_str = request.form.get("request")

    if selected_status_str is None:
        h.flash_error("Estado no seleccionado.")
        return redirect(
            f"/institutions/{institution_id}/services/{service_id}/requests"
        )
    else:
        selected_status = RequestStatus(selected_status_str)
        RequestService.update_state_request(request_id, selected_status)
        h.flash_success("Solicitud actualizada correctamente.")

    return redirect(
        f"/institutions/{institution_id}/services/{service_id}/requests"
    )


@bp.get("/<int:request_id>/notes")
@h.authenticated_route(module="service_request", permissions=("show", "index"))
@h.authenticated_route()
def notes_get(institution_id: int, service_id: int, request_id: int):
    notes = RequestService.get_request_notes(request_id)
    request_details = RequestService.get_service_request_details(request_id)
    return render_template(
        "institutions/[id]/services/[id]/requests/notes.html",
        notes=notes,
        institution_id=institution_id,
        request_details=request_details,
        service_id=service_id,
        request_id=request_id,
    )


@bp.get("/<int:request_id>/notes/new")
@h.authenticated_route(module="service_request", permissions=("update",))
@h.authenticated_route()
def create_notes_get(institution_id: int, service_id: int, request_id: int):
    form = RequestNoteForm()

    return render_template(
        "institutions/[id]/services/[id]/requests/new_note.html",
        form=form,
    )


@bp.post("/<int:request_id>/notes/new")
@h.authenticated_route(module="service_request", permissions=("update",))
@h.authenticated_route()
def create_notes_post(institution_id: int, service_id: int, request_id: int):
    form = RequestNoteForm()
    user_id = g.user.id
    if form.validate():
        RequestService.create_note(
            service_request_id=request_id, **form.values(), user_id=user_id
        )
        h.flash_success("Nota creada correctamente.")
        return redirect(
            f"/institutions/{institution_id}/services/{service_id}/requests/{request_id}/notes"  # noqa: E501
        )
    return render_template(
        "institutions/[id]/services/[id]/requests/new_note.html",
        form=form,
    )
