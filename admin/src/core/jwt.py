from flask import Flask
from flask_jwt_extended import JWTManager

jwt = JWTManager()


def init_app(app: Flask) -> None:
    jwt.init_app(app)
