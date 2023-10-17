from flask import Blueprint, g, redirect, render_template

from src.web.controllers import _helpers as h

bp = Blueprint("requests", __name__)


@bp.get("/")
@h.authenticated_route()
def requests_get():
    if len(g.institutions) == 0:
        return redirect("/")

    return render_template("institutions/index.html")


@bp.get("/new")
@h.authenticated_route()
def requests_new_get(institution_id: int):
    requests = []

    return render_template("admin/requests.html", requests=requests)


@bp.get("/<int:request_id>")
@h.authenticated_route()
def requests_id_get(institution_id: int):
    requests = []

    return render_template("admin/requests.html", requests=requests)


@bp.get("/<int:request_id>/edit")
@h.authenticated_route()
def requests_id_edit_get(institution_id: int):
    requests = []

    return render_template("admin/requests.html", requests=requests)
