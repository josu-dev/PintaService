import typing as t

from flask import Blueprint, redirect, render_template, request, session

from src.core.enums import GenderOptions
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.user import ProfileUpdateForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.get("/setting")
@h.authenticated_route()
def user_setting_get():
    user = UserService.get_by_email(t.cast(str, session["user"]))
    form = ProfileUpdateForm(obj=user)

    genders = [(choice.name, choice.value) for choice in GenderOptions]

    return render_template(
        "user/setting.html",
        user=user,
        genders=genders,
        form=form,
    )


@bp.post("/setting")
@h.authenticated_route()
def user_setting_post():
    form = ProfileUpdateForm(request.form)
    user_setting = UserService.get_by_email(t.cast(str, session.get("user")))
    if form.validate():
        try:
            id_user = t.cast(int, session.get("user_id"))
            user_setting = UserService.update_user(id_user, **form.values())
            if user_setting is None:
                return redirect("/login")
            form.process(obj=user_setting)
            h.flash_success("Configuracion actualizada")
            status_code = status.HTTP_200_OK
        except UserService.UserServiceError as e:
            h.flash_error(e.message)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    genders = [(choice.name, choice.value) for choice in GenderOptions]
    return (
        render_template(
            "user/setting.html",
            user=user_setting,
            genders=genders,
            form=form,
        ),
        status_code,
    )
