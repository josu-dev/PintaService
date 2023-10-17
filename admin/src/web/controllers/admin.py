from flask import Blueprint, flash, g, redirect, render_template, request

from src.core.enums import GenderOptions
from src.core.models.service import ServiceType
from src.services.database import DatabaseService
from src.services.institution import InstitutionService
from src.services.service import ServiceService
from src.services.site import SiteService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.institution import InstitutionForm
from src.web.forms.service import ServiceForm
from src.web.forms.site import SiteUpdateForm
from src.web.forms.user import ProfileUpdateForm

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
@h.authenticated_route(module="setting", permissions=("show", "update"))
def index_get():
    return render_template("admin/index.html")


@bp.get("/site_config")
@h.authenticated_route(module="setting", permissions=("show",))
def site_config_get():
    site_config = SiteService.get_site_config()
    form = SiteUpdateForm(request.form, obj=site_config)
    return render_template("admin/site_config.html", form=form)


@bp.post("/site_config")
@h.authenticated_route(module="setting", permissions=("update",))
def site_config_post():
    form = SiteUpdateForm(request.form)
    if form.validate():
        try:
            site_config = SiteService.update_site_config(**form.values())
            form.process(obj=site_config)
            h.flash_success("Configuracion actualizada")
            status_code = status.HTTP_200_OK
        except SiteService.SiteServiceError as e:
            h.flash_error(e.message)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    return (
        render_template("admin/site_config.html", form=form),
        status_code,
    )


@bp.get("/check_db")
@h.authenticated_route()
def check_db_get():
    if DatabaseService.health_check():
        return "Database is up and running", status.HTTP_200_OK

    return "Database is not running", status.HTTP_503_SERVICE_UNAVAILABLE


@bp.route("/users", methods=["GET", "POST"])
def users():
    site_config_pages = g.site_config.page_size
    page = request.values.get("page", 1, type=int)
    per_page = request.values.get("per_page", site_config_pages, type=int)
    email = request.values.get("email")
    active = request.values.get("active")
    users, total = UserService.filter_users_by_email_and_active(
        email, active, page, per_page  # type: ignore
    )
    return render_template(
        "admin/users.html",
        users=users,
        page=page,
        per_page=per_page,
        total=total,
        email=email,
        active=active,
    )


@bp.get("/user/<int:user_id>/edit")
def user_edit_get(user_id: int):
    """Show the edit user form with his actual values"""
    user = UserService.get_user(user_id)
    genders = [(choice.name, choice.value) for choice in GenderOptions]
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect("/admin/users")

    form = ProfileUpdateForm(obj=user)
    return render_template(
        "profile.html", user=user, genders=genders, form=form
    )


@bp.post("/user/<int:user_id>/edit")
def edit_user_post(user_id: int):
    """Edit the user with the new values"""
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect("/admin/users")

    form = ProfileUpdateForm(request.form)
    if form.validate():
        UserService.update_user(user_id, **form.values())
        flash("Usuario actualizado con éxito.", "success")
        return redirect("/admin/users")

    return render_template("profile.html", user=user, form=form)


@bp.post("/user/<int:user_id>/delete")
def user_delete_post(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect("/admin/users")
    else:
        UserService.delete_user(user_id)
        flash("Usuario eliminado con éxito.", "success")
    return redirect("/admin/users")


@bp.post("/user/<int:user_id>/toggle_active")
def toggle_active(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect("/admin/users")
    else:
        UserService.toggle_active(user_id)
        if user.is_active:
            flash("Usuario activado con éxito.", "success")
        else:
            flash("Usuario desactivado con éxito.", "success")
    return redirect("/admin/users")


@bp.get("/institutions")
@h.authenticated_route(module="institution", permissions=("index",))
def show_institutions():
    institutions = InstitutionService.get_institutions()

    return render_template(
        "admin/institutions/index.html", institutions=institutions
    )


@bp.get("/institutions/new")
@h.authenticated_route(module="institution", permissions=("create",))
def institutions_new_get():
    form = InstitutionForm()

    return render_template("admin/institutions/new.html", form=form)


@bp.post("/institutions/new")
@h.authenticated_route(module="institution", permissions=("create",))
def institutions_new_post():
    form = InstitutionForm(request.form)
    if not form.validate():
        return render_template("admin/institutions/new.html", form=form)

    try:
        institution = InstitutionService.create_institution(**form.values())
    except InstitutionService.InstitutionServiceError as e:
        # TODO: handle error on creation
        h.flash_error(e.message)
        return render_template("admin/institutions/new.html", form=form)

    h.flash_success("Institución creada con éxito.")
    return redirect(f"/admin/institutions/{institution.id}")


@bp.get("/institutions/<int:institution_id>")
@h.authenticated_route(module="institution", permissions=("show", "update"))
def institutions_id_get(institution_id: int):
    institution = InstitutionService.get_institution(institution_id)
    if not institution:
        h.flash_info(f"Institución con id {institution_id} no encontrada.")
        return redirect("/admin/institutions")

    form = InstitutionForm(obj=institution)
    return render_template(
        "admin/institutions/update.html",
        form=form,
        institution=institution,
    )


@bp.post("/institutions/<int:institution_id>")
@h.authenticated_route(module="institution", permissions=("update",))
def institutions_id_post(institution_id: int):
    institution = InstitutionService.get_institution(institution_id)
    if not institution:
        h.flash_info(
            f"Institución con id {institution_id} no encontrada al actualizar."
        )
        return redirect("/admin/institutions")

    form = InstitutionForm(request.form)
    if form.validate():
        InstitutionService.update_institution(institution_id, **form.values())
        h.flash_success("Institución actualizada con éxito.")
        return redirect(f"/admin/institutions/{institution.id}")

    return render_template(
        "/admin/institutions/update.html", institution=institution, form=form
    )


@bp.post("/institutions/<int:institution_id>/delete")
@h.authenticated_route(module="institution", permissions=("destroy",))
def institution_delete_post(institution_id: int):
    institution = InstitutionService.get_institution(institution_id)
    if not institution:
        h.flash_info(
            f"Institución con id {institution_id} no encontrada al eliminar."
        )
        return redirect("/admin/institutions")

    result = InstitutionService.delete_institution(institution_id)
    if result:
        h.flash_success("Institución eliminada con éxito.")
        return redirect("/admin/institutions")

    h.flash_error("No se pudo eliminar la institución.")
    return redirect(f"/admin/institutions/{institution.id}")


@bp.post("/institutions/<int:institution_id>/enable")
@h.authenticated_route(module="institution", permissions=("activate",))
def institution_id_activate_post(institution_id: int):
    result = InstitutionService.update_institution(
        institution_id, enabled=True
    )
    if result:
        h.flash_success("Institución activada con éxito.")
    else:
        h.flash_error("No se pudo activar la institución.")

    return redirect("/admin/institutions")


@bp.post("/institutions/<int:institution_id>/disable")
@h.authenticated_route(module="institution", permissions=("deactivate",))
def institution_id_deactivate_post(institution_id: int):
    result = InstitutionService.update_institution(
        institution_id, enabled=False
    )
    if result:
        h.flash_success("Institución desactivada con éxito.")
    else:
        h.flash_error("No se pudo desactivar la institución.")

    return redirect("/admin/institutions")


@bp.route("/create_service", methods=["GET", "POST"])
def create_service():
    """Create a service form page"""
    form = ServiceForm(request.form)
    if request.method == "POST":
        ServiceService.create_service(**form.values())
        flash("Servicio creado con exito", "success")
        return redirect("/admin/services")
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

    return render_template("service/setting.html", service=service, form=form)


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
