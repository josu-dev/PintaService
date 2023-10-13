from core.enums import GenderOptions
from flask import Blueprint, flash, g, redirect, render_template, request

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


# @bp.get("/users")
# def users_get():
#     site_config_pages = g.site_config.page_size
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", site_config_pages, type=int)
#     users, total = UserService.get_users(page, per_page)
#     email = request.args.get("email", "")
#     active = request.args.get("active", "")
#     return render_template(
#         "admin/users.html",
#         users=users,
#         page=page,
#         per_page=per_page,
#         total=total,
#         email=email,
#         active=active,
#     )


# @bp.post("/users")
# def users_post():
#     site_config_pages = g.site_config.page_size
#     page = request.args.get("page", 1, type=int)
#     per_page = request.args.get("per_page", site_config_pages, type=int)
#     email = request.form.get("email")
#     active = request.form.get("active")
#     users, total = UserService.filter_users_by_email_and_active(
#         email, active, page, per_page
#     )
#     return render_template(
#         "admin/users.html",
#         users=users,
#         page=page,
#         per_page=per_page,
#         total=total,
#         email=email,
#         active=active,
#     )


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
        "user/setting.html", user=user, genders=genders, form=form
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

    return render_template("user/setting.html", user=user, form=form)


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
