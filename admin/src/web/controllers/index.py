from datetime import datetime

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.services.auth import AuthService
from src.services.user import UserService
from src.web.controllers import _helpers as h
from src.web.forms.auth import UserLogin, UserPreRegister, UserRegister

bp = Blueprint("root", __name__)


@bp.route("/", methods=["GET"])
@h.login_required()
def index():
    return render_template("index.html")


@bp.route("/logout", methods=["GET"])  # that should be done with a post
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        h.flash_info("La sesion se cerro correctamente")
    else:
        h.flash_info("No hay una sesion iniciada")
    return redirect(url_for("root.login"))


@bp.route("/login", methods=["GET", "POST"])
@h.unauthenticated_route()
def login():
    if request.method == "POST":
        form = UserLogin(request.form)
        if form.validate():
            user = AuthService.validate_email_password(**form.values())
            if not user:
                h.flash_error("Los parametros son invalidos")
                return redirect(url_for("root.login"))

            session["user"] = user.email
            h.flash_success("Se inicio sesion correctamente")
            return redirect(url_for("root.index"))

        h.flash_error("Los datos ingresados son invalidos")
    return render_template("login.html")


@bp.route("/pre_register", methods=["GET", "POST"])
@h.unauthenticated_route()
def pre_register():
    form = UserPreRegister(request.form)

    if request.method == "POST":
        if form.validate():
            AuthService.create_pre_user(**form.values())
            h.flash_success("verifique su casilla de mail")
            return redirect("/register")  # hacer el temario del mail

        h.flash_error("el mail ya esta registrado")
        return redirect(url_for("root.index"))

    return render_template("pre_register.html")


@bp.route("/register", methods=["GET", "POST"])
@h.unauthenticated_route()
def register():
    token = request.args.get("token")
    if not token:
        h.flash_info("realice el registro o revise su casilla de email")
        return redirect(url_for("root.pre_register"))

    user = AuthService.get_pre_user(token)
    if user is None:
        return redirect(url_for("root.pre_register"))

    if user.created_at.day != datetime.now().day:
        AuthService.delete_pre_user(token)
        h.flash_info("El token invalido, realice el registro nuevamente")
        return redirect(url_for("root.pre_register"))

    if request.method == "GET":
        return render_template("register.html")

    form = UserRegister(request.form)
    if not form.validate():
        return render_template("register.html")

    form_values = form.values()
    UserService.create_user(
        username=form_values["username"],
        password=form_values["password"],
        **user.asdict(
            ("email", "firstname", "lastname"),
        ),
        document_type="",
        document_number="",
        gender="",
        gender_other="",
        address="",
        phone="",
    )
    AuthService.delete_pre_user(token)
    h.flash_success("Se ha registrado exitosamente")
    return redirect(url_for("root.login"))


@bp.route("/search_user", methods=["GET"])
def search_user():
    return render_template("search_user.html")
