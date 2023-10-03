from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_app(app: Flask):
    bcrypt.init_app(app)
