from flask import Blueprint, g, redirect, render_template, request

from src.core.enums import GenderOptions
from src.services.auth import AuthService
from src.services.database import DatabaseService
from src.services.institution import InstitutionService
from src.services.site import SiteService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.institution import EmailForm, InstitutionForm
from src.web.forms.site import SiteUpdateForm
from src.web.forms.user import ProfileUpdateForm, UserCreateForm

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
    page_size = g.site_config.page_size
    page: int = request.values.get("page", 1, type=int)  # type:ignore
    per_page: int = request.values.get(  # type:ignore
        "per_page", page_size, type=int
    )
    email = request.values.get("email")
    active = request.values.get("active")

    users, total = UserService.filter_users_by_email_and_active(
        email, active, page, per_page
    )

    return render_template(
        "admin/users/index.html",
        users=users,
        page=page,
        per_page=per_page,
        total=total,
        email=email,
        active=active,
    )


@bp.get("/users/new")
@h.authenticated_route(module="user", permissions=("create",))
def users_new_get():
    form = UserCreateForm()
    genders = [(choice.name, choice.value) for choice in GenderOptions]

    return render_template("admin/users/new.html", form=form, genders=genders)


@bp.post("/users/new")
@h.authenticated_route(module="user", permissions=("create",))
def services_new_post():
    genders = [(choice.name, choice.value) for choice in GenderOptions]

    form = UserCreateForm(request.form)
    if not form.validate():
        return render_template(
            "admin/users/new.html", form=form, genders=genders
        )

    form_values = form.values()

    if UserService.exist_user_with_email(form_values["email"]):
        h.flash_error(f"Usuario con email {form_values['email']} ya existe.")
        return render_template(
            "admin/users/new.html", form=form, genders=genders
        )

    try:
        _ = UserService.create_user(**form_values)
    except UserService.UserServiceError as e:
        h.flash_error(e.message)
        return render_template(
            "admin/users/new.html", form=form, genders=genders
        )

    h.flash_success("Usuario creado exitosamente")
    return redirect("/admin/users")


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
    if not form.validate():
        return render_template("profile.html", user=user, form=form)

    UserService.update_user(user_id, **form.values())
    h.flash_success("Usuario actualizado con éxito.")
    return redirect("/admin/users")


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

    try:
        result = UserService.delete_user(user_id)
    except UserService.UserServiceError as e:
        h.flash_error(e.message)
        return redirect("/admin/users")

    if result:
        h.flash_success("Usuario eliminado con éxito.")
        return redirect("/admin/users")

    h.flash_error("No se pudo eliminar el usuario.")
    return redirect(f"/admin/users/{user.id}")


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
    site_config_pages = g.site_config.page_size
    page = request.values.get("page", 1, type=int)
    per_page = request.values.get("per_page", site_config_pages, type=int)

    institutions, total = InstitutionService.get_institutions(
        page, per_page  # type: ignore
    )

    return render_template(
        "admin/institutions/index.html",
        institutions=institutions,
        page=page,
        per_page=per_page,
        total=total,
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
    form_new_owner = EmailForm()

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
    form = EmailForm(request.form)
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
    except AuthService.AuthServiceError as e:
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
