import typing as t
import urllib.parse

from flask import (
    Blueprint,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.core.enums import DocumentTypes, GenderOptions, RegisterTypes
from src.core.google import oauth
from src.services.auth import AuthService
from src.services.mail import MailService
from src.services.user import UserService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.auth import (
    UserLogin,
    UserPreRegister,
    UserRegister,
    UserRegisterGoogle,
)
from src.web.forms.user import ProfileUpdateForm

bp = Blueprint("root", __name__)


@bp.get("/")
@h.authenticated_route()
def index_get():
    if g.user_has_permissions(("setting_show",)):
        return redirect("/admin")

    if len(g.institutions) > 0:
        return redirect("/institutions")

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
    return (
        render_template("login.html", form=form),
        status.HTTP_400_BAD_REQUEST,
    )


@bp.get("/pre_register")
@h.require_no_session()
def pre_register_get():
    form = UserPreRegister()
    redirect_to = request.args.get("redirect_to")
    return render_template(
        "pre_register.html", redirect_to=redirect_to, form=form
    )


@bp.post("/pre_register")
@h.require_no_session()
def pre_register_post():
    form = UserPreRegister(request.form)
    redirect_to_arg = request.args.get("redirect_to")
    if not form.validate():
        h.flash_error("Los datos ingresados son invalidos")
        return (
            render_template(
                "pre_register.html", redirect_to=redirect_to_arg, form=form
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    email = t.cast(str, form.email.data)
    if AuthService.exist_pre_user_with_email(
        email
    ) or UserService.get_by_email(email):
        h.flash_error("El mail ya esta registrado")
        return (
            render_template(
                "pre_register.html", redirect_to=redirect_to_arg, form=form
            ),
            status.HTTP_400_BAD_REQUEST,
        )
    register_type = RegisterTypes.MANUAL
    user = AuthService.create_pre_user(
        register_type=register_type, **form.values()
    )

    register_link = f"{request.host_url}register?token={user.token}"

    if redirect_to_arg is not None:
        if "?email=" in redirect_to_arg:
            register_link += f"&redirect_to={urllib.parse.quote(redirect_to_arg)}"  # noqa: E501
        else:
            register_link += f"&redirect_to={urllib.parse.quote(redirect_to_arg + '?email=' + user.email)}"  # noqa: E501

    MailService.send_mail(
        "Confirmacion de Registro",
        user.email,
        f'Finalice el registro entrando a <a href="{register_link}">este link</a> completando la informacion restante.',  # noqa: E501
    )
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
        redirect_to_link = request.args.get("redirect_to")
        return redirect(
            url_for("root.pre_register_get", redirect_to=redirect_to_link)
        )

    google_register = request.args.get("google")
    if (
        google_register is not None
        and user.register_type == RegisterTypes.GOOGLE
    ):
        form = UserRegisterGoogle()
        return render_template(
            "register.html",
            form=form,
            form_action="/register_google" + "?token=" + user.token,
        )

    form = UserRegister()
    return render_template(
        "register.html",
        form=form,
    )


@bp.post("/register")
@h.require_no_session()
def register_post():
    token = request.args.get("token")
    redirect_to_link = request.args.get("redirect_to")
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
        return redirect(
            url_for("root.pre_register_get", redirect_to=redirect_to_link)
        )

    form = UserRegister(request.form)
    if not form.validate():
        h.flash_info("Los datos ingresados son invalidos")
        return (
            render_template(
                "register.html", redirect_to=redirect_to_link, form=form
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    form_values = form.values()
    if UserService.exist_user_with_username(form_values["username"]):
        h.flash_info("El nombre de usuario esta utilizado")
        return (
            render_template(
                "register.html", redirect_to=redirect_to_link, form=form
            ),
            status.HTTP_400_BAD_REQUEST,
        )

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

    if redirect_to_link is not None:
        return redirect(redirect_to_link)

    h.flash_success("Se ha registrado exitosamente")
    return redirect("/login")


@bp.post("/register_google")
@h.require_no_session()
def register_google_post():
    token = request.args.get("token")
    if not token:
        h.flash_info("Realice el registro")
        return redirect(url_for("root.login_get"))

    user = AuthService.get_pre_user_by_token(token)
    if user is None:
        h.flash_info("Realice el registro")
        return redirect(url_for("root.login_get"))

    form = UserRegisterGoogle(request.form)
    if not form.validate():
        h.flash_info("Los datos ingresados son invalidos")
        return (
            render_template("register.html", form=form),
            status.HTTP_400_BAD_REQUEST,
        )

    form_values = form.values()
    if UserService.exist_user_with_username(form_values["username"]):
        h.flash_info("El nombre de usuario esta utilizado")
        return (
            render_template("register.html", form=form),
            status.HTTP_400_BAD_REQUEST,
        )

    UserService.create_user(
        username=form_values["username"],
        password=form_values["password"],
        firstname=form_values["firstname"],
        lastname=form_values["lastname"],
        email=user.email,
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


@bp.get("/login_callback")
def google_login_get():  # type: ignore
    return oauth.google.authorize_redirect(  # type: ignore
        url_for("root.google_login_post", _external=True)
    )


@bp.get("/login_callback_get")
def google_login_post():
    token = oauth.google.authorize_access_token()  # type: ignore

    if token is None:
        h.flash_success("Parametros invalidos")
        return redirect("/login")

    user_info = token["userinfo"]  # type: ignore
    user = UserService.get_by_email(user_info["email"])  # type: ignore
    if user:
        session["user"] = user.email
        session["user_id"] = user.id
        if AuthService.user_is_site_admin(user.id):
            session["is_admin"] = True
        h.flash_success("Se inicio sesion correctamente")
        return redirect(url_for("root.index_get"))

    user = AuthService.get_pre_user_by_email(user_info["email"])  # type:ignore
    if user:
        h.flash_info(
            "Complete el registro para tener acceso a las funcionalidades"
        )
        return redirect(
            url_for("root.register_get") + f"?token={user.token}&google=google"
        )

    register_type = RegisterTypes.GOOGLE

    user = AuthService.create_pre_user(
        firstname="",
        lastname="",
        email=user_info["email"],  # type: ignore
        register_type=register_type,
    )

    h.flash_info(
        "Complete el registro para tener acceso a las funcionalidades"
    )
    return redirect(
        url_for("root.register_get") + f"?token={user.token}&google=google"
    )


bp.get("/push_main")(lambda: (render_template("_errors/451.html"), 451))
