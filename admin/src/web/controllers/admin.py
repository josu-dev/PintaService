from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.services.database import DatabaseService
from src.services.site import SiteService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.site import SiteUpdateForm
from src.web.forms.user import UserCreateForm, UserUpdateForm

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


@bp.get("/user")
def user_get():
    form = UserUpdateForm(request.form)
    return render_template("admin/user.html", form=form)


@bp.post("/user")
def user_post():
    form = UserCreateForm(request.form)
    if form.validate():
        UserService.create_user(**form.values())
        h.flash_success("Usuario creado")
        status_code = status.HTTP_200_OK
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    return (
        render_template("admin/user.html", form=form),
        status_code,
    )


@bp.get("/users")
def users_get():
    users = UserService.get_users()
    return render_template("admin/users.html", users=users)


@bp.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id: int):
    """Edit an existing user"""
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.show_users"))

    form = UserUpdateForm(request.form, obj=user)

    if request.method == "POST" and form.validate():
        UserService.update_user(user_id, **form.values())
        flash("Usuario actualizado con éxito.", "success")
        return redirect(url_for("admin.show_users"))

    return render_template("admin/edit_user.html", user=user, form=form)


@bp.route("/delete_user/<int:user_id>", methods=["GET"])
def delete_user(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.show_users"))
    else:
        UserService.delete_user(user_id)
        flash("Usuario eliminado con éxito.", "success")
    return redirect(url_for("admin.show_users"))


@bp.route("/toggle_active/<int:user_id>", methods=["GET"])
def toggle_active(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin.show_users"))
    else:
        UserService.toggle_active(user_id)
        if user.is_active:
            flash("Usuario activado con éxito.", "success")
        else:
            flash("Usuario desactivado con éxito.", "success")
    return redirect(url_for("admin.show_users"))
