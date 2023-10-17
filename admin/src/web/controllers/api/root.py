from flask import Blueprint

from src.services.user import UserService
from src.web.controllers.api import base
from src.web.forms import api as api_forms

bp = Blueprint("root", __name__)


@bp.post("/auth")
@base.validation(api_forms.AuthForm)
def auth_post(body: api_forms.AuthFormValues):
    user = UserService.validate_email_password(body["email"], body["password"])
    if not user:
        return {"result": "fail"}

    return {"result": "success"}


# TODO: remove this mock
def get_institutions(offset: int, limit: int):
    return (
        {
            "name": "Institución #1",
            "information": "Información adicional",
            "address": "Calle 50 N° 1234",
            "location": "latitude, longitude",
            "web": "www.institucion1.com",
            "days_and_opening_hours": "Lunes a viernes de 8 a 18hs",
            "email": "info@institution.com",
            "enabled": False,
        },
    )


@bp.get("/institutions")
@base.validation(api_forms.InstitutionsForm, "GET", content_type=False)
def institutions_get(args: api_forms.InstitutionsFormValues):
    page = args["page"]
    per_page = args["per_page"]
    offset = (page - 1) * per_page
    try:
        # TODO: change this to a real implementation
        institutions = get_institutions(offset, per_page)
    except Exception:
        return base.API_INTERNAL_SERVER_ERROR_RESPONSE

    total = 80
    return {
        "data": institutions,
        "page": page,
        "per_page": per_page,
        "total": total,
    }
