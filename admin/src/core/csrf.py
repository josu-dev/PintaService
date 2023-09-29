from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def init_app(app: Flask):
    csrf.init_app(app)
