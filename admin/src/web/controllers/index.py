from flask import Blueprint, render_template, request, redirect, url_for
from src.web.forms.user import UserPreRegister

bp = Blueprint("root", __name__)


@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/pre_register", methods=["GET", "POST"])
def pre_register():
    form = UserPreRegister(request.form)

    if request.method == "POST":
        if form.validate():
            return redirect("/register")
            pass  # hacer el temario del mail y tirar flash
        else:
            return redirect(url_for("root.index"))
            pass  # hacer pull y tirar flash

    return render_template("pre_register.html")


@bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


@bp.route("/search_user", methods=["GET"])
def search_user():
    return render_template("search_user.html")
