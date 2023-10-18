from flask import Blueprint, flash, g, redirect, render_template, request

from src.core.enums import GenderOptions
from src.core.models.service import ServiceType
from src.services.auth import AuthService
from src.services.database import DatabaseService
from src.services.institution import InstitutionService
from src.services.service import ServiceService
from src.services.site import SiteService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.institution import InstitutionForm, InstitutionOwnerForm
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


@bp.get("/users")
@h.authenticated_route(
    module="user", permissions=("index", "create", "update", "destroy")
)
def users_get():
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


@bp.get("/users/<int:user_id>")
@h.authenticated_route(module="user", permissions=("show", "update"))
def users_id_get(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        h.flash_error(f"Usuario con id {user_id} no encontrado.")
        return redirect("/admin/users")

    genders = [(choice.name, choice.value) for choice in GenderOptions]

    form = ProfileUpdateForm(obj=user)
    return render_template(
        "profile.html", user=user, genders=genders, form=form
    )


@bp.post("/users/<int:user_id>")
@h.authenticated_route(module="user", permissions=("update",))
def users_id_post(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        h.flash_error(f"Usuario con id {user_id} no encontrado al actualizar.")
        return redirect("/admin/users")

    form = ProfileUpdateForm(request.form)
    if form.validate():
        UserService.update_user(user_id, **form.values())
        h.flash_success("Usuario actualizado con éxito.")
        return redirect("/admin/users")

    return render_template("profile.html", user=user, form=form)


@bp.post("/users/<int:user_id>/delete")
@h.authenticated_route(module="user", permissions=("destroy",))
def users_id_delete_post(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        h.flash_error(f"Usuario con id {user_id} no encontrado al eliminar.")
        return redirect("/admin/users")

    if AuthService.user_is_site_admin(user_id):
        h.flash_error("No se puede eliminar un usuario administrador.")
        return redirect("/admin/users")

    # TODO: check if user has been deleted
    UserService.delete_user(user_id)
    h.flash_success("Usuario eliminado con éxito.")

    return redirect("/admin/users")


@bp.post("/users/<int:user_id>/toggle_active")
@h.authenticated_route(module="user", permissions=("update",))
def users_id_toggle_active_post(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        h.flash_error(f"Usuario con id {user_id} no encontrado al actualizar.")
        return redirect("/admin/users")

    UserService.toggle_active(user_id)
    if user.is_active:
        h.flash_success("Usuario activado con éxito.")
    else:
        h.flash_success("Usuario desactivado con éxito.")

    return redirect("/admin/users")


@bp.get("/institutions")
@h.authenticated_route(module="institution", permissions=("index",))
def institutions_get():
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

    institution_owners = InstitutionService.get_institution_owners(
        institution_id
    )
    form = InstitutionForm(obj=institution)
    form_new_owner = InstitutionOwnerForm()

    return render_template(
        "admin/institutions/update.html",
        form=form,
        form_new_owner=form_new_owner,
        institution=institution,
        institution_owners=institution_owners,
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
def institutions_id_delete_post(institution_id: int):
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
def institutions_id_enable_post(institution_id: int):
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
def institutions_id_disable_post(institution_id: int):
    result = InstitutionService.update_institution(
        institution_id, enabled=False
    )
    if result:
        h.flash_success("Institución desactivada con éxito.")
    else:
        h.flash_error("No se pudo desactivar la institución.")

    return redirect("/admin/institutions")


@bp.post("/institutions/<int:institution_id>/add_owner")
@h.authenticated_route(module="institution", permissions=("update",))
def institutions_id_add_owner_post(institution_id: int):
    form = InstitutionOwnerForm(request.form)
    if not form.validate():
        h.flash_error("Formulario invalido.")
        return redirect(f"/admin/institutions/{institution_id}")

    new_owner = UserService.get_by_email(form.email.data)  # type: ignore
    if not new_owner:
        h.flash_error(f"Usuario con email {form.email.data} no encontrado.")
        return redirect(f"/admin/institutions/{institution_id}")

    if AuthService.user_is_site_admin(new_owner.id):
        h.flash_error(
            f"Usuario con email {form.email.data} no puede ser dueño \
            de una institución."
        )
        return redirect(f"/admin/institutions/{institution_id}")

    try:
        result = AuthService.add_institution_role(
            "OWNER", new_owner.id, institution_id
        )
    except InstitutionService.InstitutionServiceError as e:
        # TODO: handle error on creation
        h.flash_error(e.message)
        return redirect(f"/admin/institutions/{institution_id}")

    if result:
        h.flash_success("Dueño asignado con éxito.")
    else:
        h.flash_error("No se pudo asignar dueño a la institución.")

    return redirect(f"/admin/institutions/{institution_id}")


@bp.post("/institutions/<int:institution_id>/remove_owner/<int:owner_id>")
@h.authenticated_route(module="institution", permissions=("update",))
def institutions_id_remove_owner_id_post(institution_id: int, owner_id: int):
    current_owners = InstitutionService.get_institution_owners(institution_id)
    if len(current_owners) == 0:
        h.flash_error("La institución no tiene un dueño asignado.")
        return redirect(f"/admin/institutions/{institution_id}")

    if not any(owner.id == owner_id for owner in current_owners):
        h.flash_error("El usuario no es dueño de la institución.")
        return redirect(f"/admin/institutions/{institution_id}")

    result = AuthService.remove_institution_role(
        owner_id, institution_id, "OWNER"
    )

    if result:
        h.flash_success("Dueño removido con éxito.")
    else:
        h.flash_error("No se pudo remover dueño de la institución.")

    return redirect(f"/admin/institutions/{institution_id}")


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


@bp.route("/create_service/<int:institution_id>", methods=["GET", "POST"])
def create_service_view(institution_id: int):
    """Create a service form page"""
    form = ServiceForm(request.form)
    if request.method == "POST":
        
        service_data = form.values()
        service_data["institution_id"] = institution_id
        ServiceService.create_service(**service_data)

        flash("Servicio creado con éxito", "success")
        return redirect(f"/admin/services/{institution_id}")
    return render_template("admin/create_service.html", form=form)


@bp.route(
    "/other_services", defaults={"institution_id": None}, methods=["GET"]
)
@bp.route("/other_services/<int:institution_id>", methods=["GET"])
def show_other_services(institution_id):
    """Show services for a specific institution or all services if no institution specified"""
    if institution_id:
        services = ServiceService.get_institution_services(institution_id)
    else:
        services = ServiceService.get_services()

    return render_template("admin/services.html", services=services)
