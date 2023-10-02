from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from src.web.forms.user import UserPreRegister
from src.services.auth import AuthService
from src.web.forms.auth import UserLogin
from src.web.controllers import _helpers as h

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


@bp.route("/register", methods=["GET"])
def register():
    # if()
    return render_template("register.html")


@bp.route("/search_user", methods=["GET"])
def search_user():
    return render_template("search_user.html")
