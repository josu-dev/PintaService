import typing as t

from flask import Blueprint, render_template, session

from src.services.user import UserService
from src.web.controllers import _helpers as h
from src.web.forms.user import UserUpdateForm

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/setting", methods=["GET", "POST"])
@h.login_required()
def user_setting():
    # if request.method == "GET":

    user = UserService.get_by_email(t.cast(str, session["user"]))
    form = UserUpdateForm(obj=user)
    genders = (
        ("male", "Hombre"),
        ("female", "Mujer"),
        ("other", "Otro"),
        ("none", "Prefiero no elegir"),
    )
    return render_template(
        "user/setting.html",
        user=user,
        genders=genders,
        form=form,
    )
    # if not form.validate():
    #     h.flash_error("Los datos ingresados son invalidos")
    #     return render_template("search_user.html")
    # UserService.update_user(**form.values())
