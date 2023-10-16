import typing as t
from functools import wraps

import flask
from flask import typing as tf
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
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if not is_authenticated(flask.session):
                if message:
                    flash_info(message)
                return flask.redirect(flask.url_for("root.login"))

            return func(*args, **kwargs)

        return t.cast(TRoute, wrapper)

    return decorator


def unauthenticated_route(
    message: t.Union[str, t.Literal[False]] = "",
) -> t.Callable[[TRoute], TRoute]:
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if is_authenticated(flask.session):
                if message:
                    flash_info(message)
                return flask.redirect("/")

            return func(*args, **kwargs)

        return t.cast(TRoute, wrapper)

    return decorator


def authenticated_route(
    module: str = "",
    permissions: t.Tuple[str, ...] = tuple(),
) -> t.Callable[[TRoute], TRoute]:
    _permissions = tuple(
        f"{module}_{permission}" for permission in permissions
    )

    def has_permissions(required: t.Tuple[str, ...]) -> bool:
        user_permissions: t.Tuple[str, ...] = (
            flask.g.user_permissions or tuple()
        )

        return all(
            required_permission in user_permissions
            for required_permission in required
        )

    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if flask.session.get("user") is None:
                return flask.redirect("/login")

            if (
                flask.g.user is not None
                and not flask.g.user.is_active
                and not has_permissions(("user_update",))
            ):
                return flask.redirect("/account_disabled")

            flask.g.user_has_permissions = has_permissions

            if not has_permissions(_permissions):
                return flask.redirect("/")

            return func(*args, **kwargs)

        return wrapper  # type: ignore

    return decorator
