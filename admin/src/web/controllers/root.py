import typing as t

from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.core.enums import DocumentTypes, GenderOptions
from src.services.auth import AuthService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.auth import UserLogin, UserPreRegister, UserRegister
from src.web.forms.user import ProfileUpdateForm

bp = Blueprint("root", __name__)


@bp.get("/")
@h.authenticated_route()
def index_get():
    if len(g.institutions) > 0 and g.user_has_permissions(
        ("institution_index",)
    ):
        return redirect("/admin/institutions")

    return render_template("index.html")


@bp.post("/logout")
def logout_post():
    if session.get("user"):
        del session["user"]
        del session["user_id"]
        if session.get("is_admin"):
            del session["is_admin"]
        session.clear()
        h.flash_info("La sesion se cerro correctamente")
        return redirect(url_for("root.login_get"))
    session.clear()
    h.flash_info("No hay una sesion iniciada")
    return redirect(url_for("root.login_get"))


@bp.get("/login")
@h.require_no_session()
def login_get():
    form = UserLogin()
    return render_template("login.html", form=form)


@bp.post("/login")
@h.require_no_session()
def login_post():
    form = UserLogin(request.form)
    if form.validate():
        user = UserService.validate_email_password(**form.values())
        if user:
            session["user"] = user.email
            session["user_id"] = user.id
            if AuthService.user_is_site_admin(user.id):
                session["is_admin"] = True

            h.flash_success("Se inicio sesion correctamente")
            return redirect(url_for("root.index_get"))

    h.flash_error("Los datos ingresados son invalidos")

    return render_template("login.html", form=form)


@bp.get("/pre_register")
@h.require_no_session()
def pre_register_get():
    form = UserPreRegister()
    return render_template("pre_register.html", form=form)


@bp.post("/pre_register")
@h.require_no_session()
def pre_register_post():
    form = UserPreRegister(request.form)
    if not form.validate():
        h.flash_error("Los datos ingresados son invalidos")
        return render_template("pre_register.html", form=form)

    email = t.cast(str, form.email.data)
    if AuthService.exist_pre_user_with_email(
        email
    ) or UserService.get_by_email(email):
        h.flash_error("El mail ya esta registrado")
        return render_template("pre_register.html", form=form)

    AuthService.create_pre_user(**form.values())
    return render_template("info_register.html")


@bp.get("/register")
@h.require_no_session()
def register_get():
    token = request.args.get("token")
    if not token:
        h.flash_info("Realice el registro o revise su casilla de email")
        return redirect(url_for("root.login_get"))

    user = AuthService.get_pre_user_by_token(token)
    if user is None:
        h.flash_info("Realice el registro o revise su casilla de email")
        return redirect(url_for("root.login_get"))

    if AuthService.token_expired(user.created_at):
        AuthService.delete_pre_user(token)
        h.flash_info("El token expiro, realice el registro nuevamente")
        return redirect(url_for("root.pre_register_get"))

    form = UserRegister()
    return render_template("register.html", form=form)


@bp.post("/register")
@h.require_no_session()
def register_post():
    token = request.args.get("token")
    if not token:
        h.flash_info("Realice el registro o revise su casilla de email")
        return redirect(url_for("root.login_get"))

    user = AuthService.get_pre_user_by_token(token)
    if user is None:
        h.flash_info("Realice el registro o revise su casilla de email")
        return redirect(url_for("root.login_get"))

    if AuthService.token_expired(user.created_at):
        AuthService.delete_pre_user(token)
        h.flash_info("El token expiro, realice el registro nuevamente")
        return redirect(url_for("root.pre_register_get"))

    form = UserRegister(request.form)
    if not form.validate():
        h.flash_info("Los datos ingresados son invalidos")
        return render_template("register.html", form=form)

    form_values = form.values()
    if UserService.exist_user_with_username(form_values["username"]):
        h.flash_info("El nombre de usuario esta utilizado")
        return render_template("register.html", form=form)

    UserService.create_user(
        username=form_values["username"],
        password=form_values["password"],
        **user.asdict(
            ("email", "firstname", "lastname"),
        ),
        document_type=DocumentTypes.DNI,
        document_number="",
        gender=GenderOptions.NOT_SPECIFIED,
        gender_other="",
        address="",
        phone="",
    )
    AuthService.delete_pre_user(token)
    h.flash_success("Se ha registrado exitosamente")
    return redirect(url_for("root.login_get"))


@bp.get("/account_disabled")
@h.require_session()
def account_disabled_get():
    return render_template("account_disabled.html")


@bp.get("/profile")
@h.authenticated_route()
def user_setting_get():
    user = UserService.get_by_email(t.cast(str, session["user"]))
    form = ProfileUpdateForm(obj=user)

    genders = [(choice.name, choice.value) for choice in GenderOptions]

    return render_template(
        "profile.html",
        user=user,
        genders=genders,
        form=form,
    )


@bp.post("/profile")
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
            "profile.html",
            user=user_setting,
            genders=genders,
            form=form,
        ),
        status_code,
    )
