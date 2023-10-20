import typing as t

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.core.models import all_models  # pyright: ignore # noqa: F401
from src.core.models import base

db = SQLAlchemy(model_class=base.BaseModel)


def init_app(app: Flask) -> None:
    db.init_app(app)
    config_db(app)


def config_db(app: Flask) -> None:
    @app.teardown_request
    def close_session(exception: t.Union[BaseException, None] = None):
        db.session.close()


def reset_db() -> None:
    """Resets the database.

    This function drops all the tables and creates them again.
    """
    db.drop_all()
    db.create_all()
