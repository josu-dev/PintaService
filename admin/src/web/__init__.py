from dotenv import load_dotenv
from flask import Flask, render_template, request
from werkzeug import exceptions

from src.config import config
from src.core import db, seed
from src.services.site import SiteService


def create_app(env: str = "development", static_folder: str = "../../static"):
    if env == "development":
        load_dotenv()

    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )

    app.config.from_object(config.Config)

    db.init_db(app)

    from src.web.pages import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)

    @app.before_request
    def hook():
        if (
            not SiteService.maintenance_active()
            or request.path.startswith("/api")
            or request.args.get("maintenance") != "true"
        ):
            return None

        if request.method == "GET" and (
            request.path.startswith("/login")
            or request.path.startswith("/static")
        ):
            return None

        return (
            render_template(
                "maintenance.html",
                maintenance_message=SiteService.maintenance_message(),
            ),
            503,
        )

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
