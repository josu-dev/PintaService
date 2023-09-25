from dotenv import load_dotenv
from flask import Flask, render_template
from sqlalchemy.sql import text
from werkzeug import exceptions

from src.core import db
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

    @app.get("/register")
    def register():
        return render_template("register.html")

    return app
