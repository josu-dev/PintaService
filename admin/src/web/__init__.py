from dotenv import load_dotenv
from flask import Flask, render_template, request
from sqlalchemy.sql import text
from werkzeug import exceptions

from src.core import db, seed
from src.services.site import SiteService
from src.web.config import Config


def create_app(env: str = "development", static_folder: str = "../../static"):
    if env == "development":
        load_dotenv()

    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )

    app.config.from_object(Config)

    db.init_db(app)

    @app.get("/")
    def home():
        return render_template("home.html")

    @app.route("/site_config", methods=["GET", "POST"])
    def site_config():
        if request.method == "POST":
            page_size = request.form.get("page_size", type=int)
            contact_info = request.form.get("contact_info")
            maintenance_active = request.form.get(
                "maintenance_active", type=bool
            )
            maintenance_message = request.form.get("maintenance_message")
            site_config = SiteService.update_site_config(
                page_size=page_size,
                contact_info=contact_info,
                maintenance_active=maintenance_active,
                maintenance_message=maintenance_message,
            )
        else:
            site_config = SiteService.get_site_config()

        return render_template("site_config.html", site_config=site_config)

    @app.get("/ping_db")
    def ping_db():
        with db.db.get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return "OK"

    @app.errorhandler(404)
    def page_not_found(error: exceptions.NotFound):
        return (
            render_template(
                "error.html",
                error_code="404",
                error_message="Página no encontrada",
            ),
            404,
        )

    @app.cli.command("reset_db")  # pyright: ignore[reportUnknownMemberType]
    def reset_db():
        """
        Reset the database.
        Clear all tables and create them again.
        """
        db.reset_db()

    @app.cli.command("seed_db")  # pyright: ignore[reportUnknownMemberType]
    def seed_db():
        """
        Seed the database.
        """
        seed.seed_db()

    return app
