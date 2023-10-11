from flask import Blueprint

from src.web.controllers.api import root

bp = Blueprint("api", __name__, url_prefix="/api")


bp.register_blueprint(root.bp)
