from flask import Blueprint

from src.web.controllers.api import _base, root

_blueprints = (root.bp,)

bp = Blueprint("api", __name__, url_prefix="/api")

for blueprint in _blueprints:
    bp.register_blueprint(blueprint)


APIError = _base.BaseAPIError

API_NOT_FOUND_RESPONSE = _base.API_NOT_FOUND_RESPONSE
API_METHOD_NOT_ALLOWED_RESPONSE = _base.API_METHOD_NOT_ALLOWED_RESPONSE


def handle_api_error(e: _base.BaseAPIError):
    return (
        e.asdict(),
        e.status_code,
    )
