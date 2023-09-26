from flask import Blueprint, render_template, request

from src.services.database import DatabaseService
from src.services.site import SiteService

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
def index():
    return render_template("admin/index.html")


@bp.route("/site_config", methods=["GET", "POST"])
def site_config():
    if request.method == "POST":
        page_size = request.form.get("page_size", type=int)
        contact_info = request.form.get("contact_info")
        maintenance_active = request.form.get("maintenance_active", type=bool)
        maintenance_message = request.form.get("maintenance_message")
        site_config = SiteService.update_site_config(
            page_size=page_size,
            contact_info=contact_info,
            maintenance_active=maintenance_active,
            maintenance_message=maintenance_message,
        )
    else:
        site_config = SiteService.get_site_config()

    return render_template("admin/site_config.html", site_config=site_config)


@bp.route("/ping_db", methods=["GET"])
def ping_db():
    if DatabaseService.ping():
        return "Database connection successful"

    return "Database connection failed", 500
