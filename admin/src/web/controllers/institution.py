from flask import Blueprint, g, redirect, render_template, request

from src.services.auth import AuthService
from src.services.institution import InstitutionService
from src.services.user import UserService
from src.web.controllers import _helpers as h
from src.web.forms.institution import EmailForm

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
    print("entre", flush=True)
    if not (
        g.user_has_permissions(
            (
                "user_institution_create",
                "user_institution_destroy",
                "user_institution_index",
                "user_institution_update",
            )
        )
    ):
        if g.user_has_permissions(("services_index",)):
            return redirect(f"/institutions/{institution_id}/services")

        return redirect("/")

    page_size = g.site_config.page_size
    page: int = request.values.get("page", 1, type=int)  # type:ignore
    per_page: int = request.values.get(  # type:ignore
        "per_page", page_size, type=int
    )
    users, total = InstitutionService.get_institution_users(
        institution_id, page=page, per_page=per_page
    )
    institution = InstitutionService.get_institution(institution_id)
    roles = [
        ("INSTITUTION_MANAGER", "Manager"),
        ("INSTITUTION_OPERATOR", "Operador"),
    ]
    form_new_user = EmailForm()
    return render_template(
        "institutions/[id]/index.html",
        form_new_user=form_new_user,
        users=users,
        institution_id=institution_id,
        institution=institution,
        page=page,
        total=total,
        per_page=per_page,
        roles=roles,
    )


@h.authenticated_route(module="user_institution", permissions=("update",))
@bp.post("/<int:institution_id>/edit/role")
@h.authenticated_route()
def id_edit_role_post(institution_id: int):
    """Update a request."""
    user_id = request.form.get("user_id")
    if not user_id:
        h.flash_error("Usuario no encontrado.")
        return redirect(f"/institutions/{institution_id}")

    selected_role_str = request.form.get("role")

    if selected_role_str is None:
        h.flash_error("Rol no seleccionado.")
        return redirect(f"/institutions/{institution_id}")

    selected_role = InstitutionService.get_rol(selected_role_str)

    if selected_role is None:
        h.flash_error("El rol no existe.")
        return redirect(f"/institutions/{institution_id}")

    if InstitutionService.update_institution_role(
        institution_id, int(user_id), selected_role.id
    ):
        h.flash_success("Rol actualizado correctamente.")
    else:
        h.flash_success("El rol no pudo ser actualizado.")
    return redirect(f"/institutions/{institution_id}")


@bp.post("/<int:institution_id>/delete/user")
@h.authenticated_route(module="user_institution", permissions=("destroy",))
def id_delete_user(institution_id: int):
    user_id = request.form.get("user_id")
    if not user_id:
        h.flash_error("Usuario no encontrado.")
        return redirect(f"/institutions/{institution_id}")

    InstitutionService.delete_institution_user(institution_id, int(user_id))
    if InstitutionService.delete_institution_user(
        institution_id, int(user_id)
    ):
        h.flash_success("Solicitud actualizada correctamente.")
        return redirect(f"/institutions/{institution_id}")

    h.flash_success("No se pudo borrar el usuario.")
    return redirect(f"/institutions/{institution_id}")


@bp.post("/<int:institution_id>/add/user")
@h.authenticated_route(module="user_institution", permissions=("create",))
def id_add_user(institution_id: int):
    form = EmailForm(request.form)
    if not form.validate():
        h.flash_error("Formulario invalido.")
        return redirect(f"/institutions/{institution_id}")

    new_user = UserService.get_by_email(form.email.data)  # type: ignore
    if not new_user:
        h.flash_error(f"Usuario con email {form.email.data} no encontrado.")
        return redirect(f"/institutions/{institution_id}")

    if AuthService.user_is_site_admin(new_user.id):
        h.flash_error(
            f"Usuario con email {form.email.data} no puede ser usuario \
            de una institución."
        )
        return redirect(f"/institutions/{institution_id}")
    elif InstitutionService.institution_has_user(institution_id, new_user.id):
        h.flash_error(
            f"Usuario con email {form.email.data} ya es parte \
            de la institución."
        )
        return redirect(f"/institutions/{institution_id}")

    selected_role_str = request.form.get("new-role")

    if selected_role_str is None:
        h.flash_error("Rol no seleccionado.")
        return redirect(f"/institutions/{institution_id}")

    selected_role = InstitutionService.get_rol(selected_role_str)

    if selected_role is None:
        h.flash_error("El rol no existe.")
        return redirect(f"/institutions/{institution_id}")

    result = AuthService.add_institution_role(
        role=selected_role_str.split("_")[1],  # type: ignore
        user_id=new_user.id,
        institution_id=institution_id,
    )

    if result:
        h.flash_success("Usuario asignado a la institucion con éxito.")
    else:
        h.flash_error("No se pudo asignar el usuario a la institución.")

    return redirect(f"/institutions/{institution_id}")
