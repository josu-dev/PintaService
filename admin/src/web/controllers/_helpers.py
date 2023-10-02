import flask
import typing as t
from functools import wraps
from flask.sessions import SessionMixin


def flash_info(message: str):
    flask.flash(message, "info")


def flash_success(message: str):
    flask.flash(message, "success")


def flash_warning(message: str):
    flask.flash(message, "warning")


def flash_error(message: str):
    flask.flash(message, "error")


def is_authenticated(session: SessionMixin):
    return session.get("user") is not None


TRoute = t.TypeVar("TRoute", bound=t.Callable[..., t.Any])


def login_required(
    message: t.Union[
        str, t.Literal[False]
    ] = "Debes iniciar sesion para acceder",
) -> t.Callable[[TRoute], TRoute]:
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any):
            if not is_authenticated(flask.session):
                if message:
                    flash_info(message)
                return flask.redirect(flask.url_for("root.login"))

            return func(*args, **kwargs)

        return t.cast(TRoute, wrapper)

    return decorator
