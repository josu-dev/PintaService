from flask import Blueprint, g, redirect, render_template

from src.services.institution import InstitutionService
from src.services.service import ServiceService
from src.web.controllers import _helpers as h

bp = Blueprint("institutions", __name__, url_prefix="/institutions")


@bp.get("/")
@h.authenticated_route()
def index_get():
    if len(g.institutions) == 0:
        return redirect("/")

    return render_template("institutions/index.html")


@bp.get("/<int:institution_id>")
@h.authenticated_route()
def id_get(institution_id: int):
    institution = InstitutionService.get_institution(institution_id)

    return render_template(
        "institutions/[institution_id]/index.html", institution=institution
    )


@bp.get("/<int:institution_id>/edit")
@h.authenticated_route()
def id_services_get(institution_id: int):
    services = ServiceService.get_institution_services(institution_id)

    return render_template("admin/services.html", services=services)
