from flask import Blueprint, render_template, request
from web.forms.site import SiteUpdateForm
from web.forms.user import UserUpdateForm

from src.services.database import DatabaseService
from src.services.site import SiteService
from src.services.user import AuthService
from src.web.controllers import _helpers as h

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
        AuthService.create_user(**form.values())
    return render_template("admin/create_user.html", form=form)


@bp.route("/users", methods=["GET"])
def show_users():
    """Show all users in the database"""
    users = AuthService.get_users()
    return render_template("admin/users.html", users=users)
