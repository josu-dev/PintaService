from flask import Blueprint, g, redirect, render_template

from src.services.service import ServiceService
from src.web.controllers import _helpers as h

bp = Blueprint("services", __name__)


@bp.get("/")
@h.authenticated_route()
def services_get():
    if len(g.institutions) == 0:
        return redirect("/")

    return render_template("institutions/index.html")


@bp.get("/new")
@h.authenticated_route()
def services_new_get(institution_id: int):
    services = ServiceService.get_institution_services(institution_id)

    return render_template("admin/services.html", services=services)


@bp.get("/<int:service_id>")
@h.authenticated_route()
def services_id_get(institution_id: int):
    services = ServiceService.get_institution_services(institution_id)

    return render_template("admin/services.html", services=services)


@bp.get("/<int:service_id>/edit")
@h.authenticated_route()
def services_id_edit_get(institution_id: int):
    services = ServiceService.get_institution_services(institution_id)

    return render_template("admin/services.html", services=services)
