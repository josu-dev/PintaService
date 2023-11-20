from flask import Flask

from flask_session import Session
from src.core import config, cors, csrf, db, jwt
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
    cors.init_app(app)
    session.init_app(app)
    MailService.init_app(app)
    controllers.init_app(app)
    jwt.init_app(app)

    @app.cli.command("reset-db")
    def reset_db():
        """Clear all tables and create them again."""
        db.reset_db()

    @app.cli.command("seed-db")
    def seed_db():
        """Seed the database with initial data."""
        from src.core import seed

        seed.seed_db()

    @app.cli.command("test-data")
    def load_test_data():
        """Load test data for development."""
        from src.core import test_data

        test_data.load_test_data()

    @app.cli.command("full-reset")
    def full_reset():
        """
        Drops all tables, creates them again and seeds the database.
        Also loads test data for development.
        """
        from src.core import seed, test_data

        db.reset_db()
        seed.seed_db()
        test_data.load_test_data()

    return app
