from flask import Blueprint, render_template, request
from web.forms.site import SiteUpdateForm

from src.services.database import DatabaseService
from src.services.site import SiteService

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
def index():
    return render_template("admin/index.html")


@bp.route("/site_config", methods=["GET", "POST"])
def site_config():
    form = SiteUpdateForm(request.form)

    if request.method == "GET":
        site_config = SiteService.get_site_config()
        form.process(obj=site_config)

    elif request.method == "POST" and form.validate():
        site_config = SiteService.update_site_config(**form.values())
        form.process(obj=site_config)

    return render_template("admin/site_config.html", form=form)


@bp.route("/ping_db", methods=["GET"])
def ping_db():
    if DatabaseService.ping():
        return "Database connection successful"

    return "Database connection failed", 500
