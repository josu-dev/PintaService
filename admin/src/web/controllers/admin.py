from core.enums import GenderOptions
from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.services.database import DatabaseService
from src.services.site import SiteService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.site import SiteUpdateForm
from src.web.forms.user import ProfileUpdateForm

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/site_config")
def site_config_get():
    site_config = SiteService.get_site_config()
    form = SiteUpdateForm(request.form, obj=site_config)
    return render_template("admin/site_config.html", form=form)


@bp.post("/site_config")
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
def check_db_get():
    if DatabaseService.health_check():
        return "Database is up and running", status.HTTP_200_OK

    return "Database is not running", status.HTTP_503_SERVICE_UNAVAILABLE


@bp.get("/users")
def users_get():
    # Maneja la carga inicial de la página sin filtrado
    users = UserService.get_users()
    return render_template("admin/users.html", users=users)


@bp.post("/users")
def users_post():
    email = request.form.get("email")
    active = request.form.get("active")
    users = UserService.filter_users_by_email_and_active(email, active)
    return render_template("admin/users.html", users=users)


@bp.get("/user/<int:user_id>/edit")
def user_edit_get(user_id: int):
    """Show the edit user form with his actual values"""
    user = UserService.get_user(user_id)
    genders = [(choice.name, choice.value) for choice in GenderOptions]
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.users_get"))

    form = ProfileUpdateForm(obj=user)
    return render_template(
        "admin/edit_user.html", user=user, genders=genders, form=form
    )


@bp.post("/user/<int:user_id>/edit")
def edit_user_post(user_id: int):
    """Edit the user with the new values"""
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.users_get"))

    form = ProfileUpdateForm(request.form)
    if form.validate():
        UserService.update_user(user_id, **form.values())
        flash("Usuario actualizado con éxito.", "success")
        return redirect(url_for("admin.users_get"))

    return render_template("admin/edit_user.html", user=user, form=form)


@bp.post("/user/<int:user_id>/delete")
def user_delete_post(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.users_get"))
    else:
        UserService.delete_user(user_id)
        flash("Usuario eliminado con éxito.", "success")
    return redirect(url_for("admin.users_get"))


@bp.post("/user/<int:user_id>/toggle_active")
def toggle_active(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.users_get"))
    else:
        UserService.toggle_active(user_id)
        if user.is_active:
            flash("Usuario activado con éxito.", "success")
        else:
            flash("Usuario desactivado con éxito.", "success")
    return redirect(url_for("admin.users_get"))
