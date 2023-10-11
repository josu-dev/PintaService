from flask import Blueprint

from src.web.controllers.api import _api
from src.web.forms import api as api_forms

bp = Blueprint("root", __name__)


@bp.post("/auth")
@_api.validation(api_forms.AuthForm)
def auth_post(body: api_forms.AuthFormValues):
    return "auth_post"
