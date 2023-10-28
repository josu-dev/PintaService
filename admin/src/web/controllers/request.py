from flask import Blueprint, g, redirect, render_template, request

from src.core.enums import RequestStatus
from src.services.request import FilterRequestParams, RequestService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.request import (
    RequestForm,
    RequestHistoryForm,
    RequestNoteForm,
)

bp = Blueprint("requests", __name__)


@bp.get("/")
@h.authenticated_route(module="service_request", permissions=("index", "show"))
def requests_get(institution_id: int, service_id: int):
    page, per_page = h.url_pagination_args(
        default_per_page=g.site_config.page_size
    )
    request_status = request.args.get("status", "")
    user_email = request.args.get("user_email", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    kwargs: FilterRequestParams = {}
    if user_email != "":
        kwargs["user_email"] = user_email
    if request_status != "":
        kwargs["status"] = request_status  # type:ignore
    if start_date != "":
        kwargs["start_date"] = start_date
    if end_date != "":
        kwargs["end_date"] = end_date

    (
        requests,
        total,
    ) = RequestService.get_requests_filter_by_service(
        per_page=per_page,
        page=page,
        institution_id=institution_id,
        service_id=service_id,
        **kwargs,
    )

    statuses = [req_status.value for req_status in RequestStatus]
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
        status=request_status,
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
def requests_new_post(institution_id: int, service_id: int):
    form = RequestForm(request.form)
    if not form.validate():
        return (
            render_template(
                "institutions/[id]/services/[id]/requests/new.html", form=form
            ),
            status.HTTP_400_BAD_REQUEST,
        )
    try:
        RequestService.create_request(
            service_id=service_id,
            user_id=g.user.id,
            **form.values(),
        )
    except RequestService.RequestServiceError:
        h.flash_error(f"No existe el servicio con id '{service_id}'")
        return redirect(f"/institutions/{institution_id}/services")

    return redirect(
        f"/institutions/{institution_id}/services/{service_id}/requests"
    )


@bp.get("/<int:request_id>")
@h.authenticated_route(module="service_request", permissions=("update",))
def requests_id_edit_get(
    institution_id: int, service_id: int, request_id: int
):
    requestElement = RequestService.get_request(request_id)

    if not requestElement:
        h.flash_error("Solicitud no encontrada.")
        return redirect(
            f"/institutions/{institution_id}/services/{service_id}/requests"
        )

    form = RequestHistoryForm()

    return render_template(
        "institutions/[id]/services/[id]/requests/update.html",
        form=form,
        institution_id=institution_id,
        service_id=service_id,
        request_id=request_id,
    )


@bp.post("/<int:request_id>")
@h.authenticated_route(module="service_request", permissions=("update",))
def requests_id_edit_post(
    institution_id: int, service_id: int, request_id: int
):
    requestElement = RequestService.get_request(request_id)

    if not requestElement:
        h.flash_error("Solicitud no encontrada.")
        return redirect(
            f"/institutions/{institution_id}/services/{service_id}/requests"
        )
    form = RequestHistoryForm(request.form)
    if not form.validate():
        statuses = [(choice.name, choice.value) for choice in RequestStatus]

        return (
            render_template(
                "institutions/[id]/services/[id]/requests/update.html",
                form=form,
                statuses=statuses,
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    if RequestService.update_state_request(request_id, **form.values()):
        h.flash_success("Solicitud actualizada correctamente.")
    else:
        h.flash_error("No se puede cambiar la solicitud al mismo estado.")

    return redirect(
        f"/institutions/{institution_id}/services/{service_id}/requests"
    )


@bp.get("/<int:request_id>/notes")
@h.authenticated_route(module="service_request", permissions=("show", "index"))
def requests_id_notes_get(
    institution_id: int, service_id: int, request_id: int
):
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
def requests_id_notes_new_get(
    institution_id: int, service_id: int, request_id: int
):
    form = RequestNoteForm()

    return render_template(
        "institutions/[id]/services/[id]/requests/new_note.html",
        form=form,
    )


@bp.post("/<int:request_id>/notes/new")
@h.authenticated_route(module="service_request", permissions=("update",))
def requests_id_notes_new_post(
    institution_id: int, service_id: int, request_id: int
):
    form = RequestNoteForm()
    user_id = g.user.id
    if form.validate():
        RequestService.create_note(
            service_request_id=request_id, user_id=user_id, **form.values()
        )
        h.flash_success("Nota creada correctamente.")
        return redirect(
            f"/institutions/{institution_id}/services/{service_id}/requests/{request_id}/notes"  # noqa: E501
        )

    return (
        render_template(
            "institutions/[id]/services/[id]/requests/new_note.html",
            form=form,
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@bp.get("/<int:request_id>/history")
@h.authenticated_route(module="service_request", permissions=("show",))
def requests_id_notes_history_post(
    institution_id: int, service_id: int, request_id: int
):
    history = RequestService.get_request_history(request_id)

    return render_template(
        "institutions/[id]/services/[id]/requests/history.html",
        history=history,
        institution_id=institution_id,
        service_id=service_id,
        request_id=request_id,
    )
