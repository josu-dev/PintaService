import os

from flask import Config as FlaskConfig


class Config(FlaskConfig):
    # DB config
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME")

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Flask config
    SECRET_KEY = os.getenv("SECRET_KEY")  # needed for session

    # WTForms config
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")
