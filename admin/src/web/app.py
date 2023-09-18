from dotenv import load_dotenv
from flask import Flask, render_template
from sqlalchemy.sql import text
from werkzeug import exceptions

from src.core import db
from src.web.config import Config


def create_app(env: str = "development", static_folder: str = "../../static"):
    if env == "development":
        load_dotenv()
    app = Flask(__name__, static_folder=static_folder)

    app.config.from_object(Config)

    db.init_db(app)

    @app.get("/")
    def home():  # type: ignore  # noqa
        return render_template("home.html")

    @app.get("/about")
    def about():  # type: ignore  # noqa
        return render_template("about.html")

    @app.get("/contact")
    def contact():  # type: ignore  # noqa
        return render_template("contact.html")

    @app.get("/ping_db")
    def ping_db():  # type: ignore  # noqa
        with db.db.get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return "OK"

    @app.errorhandler(404)  # type: ignore  # noqa
    def page_not_found(error: exceptions.NotFound):  # type: ignore  # noqa
        return (
            render_template(
                "error.html",
                error_code="404",
                error_message="Página no encontrada",
            ),
            404,
        )

    return app
