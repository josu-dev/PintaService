from flask import Blueprint

from src.web.controllers.api import root

_blueprints = (root.bp,)

bp = Blueprint("api", __name__, url_prefix="/api")

for blueprint in _blueprints:
    bp.register_blueprint(blueprint)
