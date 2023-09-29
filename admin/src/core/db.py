from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.core.models.base import BaseModel

db = SQLAlchemy(model_class=BaseModel)


def init_app(app: Flask):
    db.init_app(app)
    config_db(app)


def config_db(app: Flask):
    @app.teardown_request
    def close_session(exception=None):  # type: ignore
        db.session.close()


def reset_db():
    """
    Reset the database.
    Clear all tables and create them again.
    """
    db.drop_all()
    db.create_all()
