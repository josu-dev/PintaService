import typing as t
from functools import wraps

import flask
from flask import typing as tf


def flash_info(message: str) -> None:
    flask.flash(message, "info")


def flash_success(message: str) -> None:
    flask.flash(message, "success")


def flash_warning(message: str) -> None:
    flask.flash(message, "warning")


def flash_error(message: str) -> None:
    flask.flash(message, "error")


TRoute = t.TypeVar("TRoute", bound=t.Callable[..., t.Any])


def require_session(
    message: t.Union[
        str, t.Literal[False]
    ] = "Debes iniciar sesion para acceder",
) -> t.Callable[[TRoute], TRoute]:
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if flask.session.get("user_id") is None:
                if message:
                    flash_info(message)

                return flask.redirect("/login")

            return func(*args, **kwargs)

        return wrapper  # pyright: ignore[reportReturnType]

    return decorator


def require_no_session(
    message: t.Union[str, t.Literal[False]] = "",
) -> t.Callable[[TRoute], TRoute]:
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if flask.session.get("user_id") is not None:
                if message:
                    flash_info(message)

                return flask.redirect("/")

            return func(*args, **kwargs)

        return wrapper  # pyright: ignore[reportReturnType]

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
            if flask.g.user is None:
                return flask.redirect("/login")

            if not flask.g.user.is_active and not has_permissions(
                ("user_update",)
            ):
                return flask.redirect("/account_disabled")

            flask.g.user_has_permissions = has_permissions

            if not has_permissions(_permissions):
                return flask.redirect("/")

            return func(*args, **kwargs)

        return wrapper  # pyright: ignore[reportReturnType]

    return decorator


def url_pagination_args(
    default_page: int = 1,
    default_per_page: int = 10,
    max_per_page: int = 100,
):
    """Get pagination params from url args.

    Page starts at 1.
    Per page starts at 1 and max is 100.

    Returns:
        Tuple[int, int]: page, per_page
    """
    arg_page = flask.request.args.get("page", "")
    arg_per_page = flask.request.args.get("per_page", "")

    page = int(arg_page) if arg_page.isdigit() else default_page
    per_page = (
        int(arg_per_page) if arg_per_page.isdigit() else default_per_page
    )

    page = page if page > 0 else default_page
    per_page = per_page if 0 < per_page <= max_per_page else default_per_page

    return page, per_page
