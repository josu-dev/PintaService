from flask import Blueprint, flash, g, redirect, render_template, request

from src.core.enums import RequestStatus
from src.services.request import RequestService
from src.web.controllers import _helpers as h
from src.web.forms.request import RequestForm

bp = Blueprint("requests", __name__)


@bp.get("/")
@h.authenticated_route(module="service_request", permissions=("index", "show"))
def requests_get(institution_id: int, service_id: int):
    if len(g.institutions) == 0:
        return redirect("/")

    site_config_pages = g.site_config.page_size
    page = request.values.get("page", 1, type=int)
    per_page = request.values.get("per_page", site_config_pages, type=int)
    requests, total = RequestService.get_requests_of(
        institution_id, page=page, per_page=per_page  # type:ignore
    )
    statuses = [status.value for status in RequestStatus]
    return render_template(
        "requests/index.html",
        requests=requests,
        institution_id=institution_id,
        service_id=service_id,
        page=page,
        total=total,
        per_page=per_page,
        statuses=statuses,
    )


@bp.get("/new")
@h.authenticated_route(module="service_request", permissions=("create",))
def requests_new_get(institution_id: int, service_id: int):
    form = RequestForm()

    return render_template("requests/new.html", form=form)


@bp.post("/new")
@h.authenticated_route(module="service_request", permissions=("create",))
def request_new_post(institution_id: int, service_id: int):
    form = RequestForm()
    if form.validate_on_submit():
        RequestService.create_request(
            institution_id=institution_id,
            service_id=service_id,
            user_id=g.user.id,
            **form.values(),
        )
        return redirect("/requests")
    return render_template("requests/new.html", form=form)


@bp.post("/<int:request_id>/edit")
def request_id_edit_post(
    institution_id: int, service_id: int, request_id: int
):
    """Update a request."""
    requestElement = RequestService.get_request(request_id)

    if not requestElement:
        print("Redirect", flush=True)
        flash("Solicitud no encontrada.", "error")
        return redirect("requests")

    selected_status_str = request.form.get("request")

    if selected_status_str is None:
        print("Redirect", flush=True)
        flash("Estado no seleccionado.", "error")
        return redirect("requests")
    else:
        print(selected_status_str, flush=True)
        selected_status = RequestStatus(selected_status_str)
        RequestService.update_state_request(request_id, selected_status)
        flash("Solicitud actualizada correctamente.", "success")

    return redirect(
        f"/institutions/{institution_id}/services/{service_id}/requests"
    )
