from flask import Blueprint, flash, redirect, render_template, request
from web.forms.site import SiteUpdateForm
from web.forms.user import UserUpdateForm

from src.services.database import DatabaseService
from src.services.site import SiteService
from src.services.user import UserService
from src.web.controllers import _helpers as h

# from web.forms.service import ServiceUpdateForm


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/site_config", methods=["GET", "POST"])
def site_config():
    form = SiteUpdateForm(request.form)

    if request.method == "GET":
        site_config = SiteService.get_site_config()
        form.process(obj=site_config)

    elif request.method == "POST" and form.validate():
        try:
            site_config = SiteService.update_site_config(**form.values())
            form.process(obj=site_config)
            h.flash_success("Site config updated")
        except SiteService.SiteServiceError as e:
            h.flash_error(e.message)

    return render_template("admin/site_config.html", form=form)


@bp.route("/check_db", methods=["GET"])
def check_db():
    if DatabaseService.health_check():
        return "Database is up and running", 200

    return "Database is not running", 500


# TODO Lucho podes tocar lo que necesites de aca para mostrar
@bp.route("/create_user", methods=["GET", "POST"])
def create_user():
    """Create an user form page"""
    form = UserUpdateForm(request.form)
    if request.method == "POST":
        UserService.create_user(**form.values())
    return render_template("admin/create_user.html", form=form)


@bp.route("/users", methods=["GET"])
def show_users():
    """Show all users in the database"""
    users = UserService.get_users()
    return render_template("admin/users.html", users=users)


from web.forms.service import ServiceForm

from src.services.service import ServiceService


@bp.route("/create_service", methods=["GET", "POST"])
def create_service():
    """Create a service form page"""
    form = ServiceForm(request.form)
    if request.method == "POST":
        ServiceService.create_service(**form.values())
    return render_template("admin/create_service.html", form=form)


@bp.route("/services", methods=["GET"])
def show_services():
    """Show all services in the database"""
    services = ServiceService.get_services()
    return render_template("admin/services.html", services=services)


@bp.post("/service/<int:service_id>/delete")
def service_delete_post(service_id: int):
    service = ServiceService.get_service(service_id)
    if not service:
        flash("Servicio no encontrado.", "error")
        return redirect("/admin/services")
    else:
        ServiceService.delete_service(service_id)
        flash("Servicio eliminado con éxito.", "success")
    return redirect("/admin/services")


# Esto no funciona de momento
@bp.post("/service/<int:service_id>/edit")
def edit_service_post(service_id: int):
    """Edit the service with the new values"""
    service = ServiceService.get_service(service_id)
    if not service:
        flash("Servicio no encontrado.", "error")
        return redirect("/admin/services")

    form = ServiceForm(request.form)
    if form.validate():
        ServiceService.update_service(service_id, **form.values())
        flash("Servicio actualizado con éxito.", "success")
        return redirect("/admin/services")

    return render_template("admin/edit_user", service=service, form=form)


from src.core.models.service import ServiceType


@bp.get("/service/<int:service_id>/edit")
def service_edit_get(service_id: int):
    """Show the edit service form with its actual values"""
    service = ServiceService.get_service(service_id)

    if not service:
        flash("Servicio no encontrado.", "error")
        return redirect("/admin/services")

    categories = [(choice.name, choice.value) for choice in ServiceType]
    form = ServiceForm(obj=service)
    return render_template(
        "service/setting.html",
        service=service,
        categories=categories,
        form=form,
    )
