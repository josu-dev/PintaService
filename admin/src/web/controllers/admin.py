from flask import Blueprint, render_template, request

from src.services.database import DatabaseService
from src.services.site import SiteService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.site import SiteUpdateForm
from src.web.forms.user import UserUpdateForm

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
    form = UserUpdateForm(request.form)
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
