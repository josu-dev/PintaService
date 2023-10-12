from flask import Flask

from flask_session import Session
from src.core import config, csrf, db, seed, test_data
from src.services.mail import MailService
from src.web import controllers

session = Session()


def create_app(env: str = "development", static_folder: str = "../../static"):
    app = Flask(
        __name__, static_folder=static_folder, template_folder="./templates"
    )

    config.init_app(app, env)
    db.init_app(app)
    csrf.init_app(app)
    session.init_app(app)
    MailService.init_app(app)
    controllers.init_app(app)

    @app.cli.command("reset_db")
    def reset_db():
        """
        Reset the database.
        Clear all tables and create them again.
        """
        db.reset_db()

    @app.cli.command("seed_db")
    def seed_db():
        """
        Seed the database.
        """
        seed.seed_db()

    @app.cli.command("test_data")
    def load_test_data():
        """
        Cositas que pasan si lees esto agustin aprobame
        soy el que se paso por vos en el stream de Fabo <3
        """
        test_data.load_test_data()

    return app
