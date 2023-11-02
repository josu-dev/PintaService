from flask import Flask
from flask_cors import CORS

cors: CORS


def init_app(app: Flask) -> None:
    global cors
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
