from flask import Blueprint

from src.web.controllers.api import _base, root

_blueprints = (root.bp,)

bp = Blueprint("api", __name__, url_prefix="/api")

for blueprint in _blueprints:
    bp.register_blueprint(blueprint)


APIError = _base.APIError

API_BAD_REQUEST_RESPONSE = _base.API_BAD_REQUEST_RESPONSE
API_NOT_FOUND_RESPONSE = _base.API_NOT_FOUND_RESPONSE
API_METHOD_NOT_ALLOWED_RESPONSE = _base.API_METHOD_NOT_ALLOWED_RESPONSE
API_INTERNAL_SERVER_ERROR_RESPONSE = _base.API_INTERNAL_SERVER_ERROR_RESPONSE


def handle_api_error(e: _base.APIError):
    return (
        {"message": e.message},
        e.status_code,
    )
