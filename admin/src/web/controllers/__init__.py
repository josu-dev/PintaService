from flask import Flask, g, render_template, request
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import exceptions

from src.services import base
from src.web.controllers import admin, api, root

_blueprints = (
    admin.bp,
    api.bp,
    root.bp,
)


def handle_not_found_error(e: exceptions.NotFound):
    if request.path.startswith("/api"):
        return api.API_NOT_FOUND_RESPONSE

    return (render_template("_errors/404.html"), 404)


def handle_method_not_allowed_error(e: exceptions.MethodNotAllowed):
    if request.path.startswith("/api"):
        return api.API_METHOD_NOT_ALLOWED_RESPONSE

    return (
        render_template(
            "_errors/default.html",
            error_code="405",
            error_title="Método http no permitido",
            error_message=f"El método \
                {request.method} no está permitido en esta página",
        ),
        405,
    )


def handle_service_error(e: base.BaseServiceError):
    return (
        render_template(
            "_errors/500.html",
            error_code="500",
            error_title="Error interno del servidor",
            error_message=e.message or "Se ha producido un error inesperado",
        ),
        500,
    )


def handle_sqlalchemy_error(e: SQLAlchemyError):
    return (
        render_template(
            "_errors/500.html",
            error_code="500",
            error_title="Error interno del servidor",
            error_message=f"Se ha producido un error inesperado \
                con la base de datos{(', ' + e.code) if e.code else ''}",
        ),
        500,
    )


def handle_internal_server_error(e: exceptions.InternalServerError):
    error_code = 500 if e.code is None else e.code
    error_message = "Se ha producido un error inesperado"
    if (
        e.original_exception
        and hasattr(e.original_exception, "message")
        and isinstance(e.original_exception.message, str)  # type: ignore
        and len(e.original_exception.message) > 0  # type: ignore
    ):
        error_message = e.original_exception.message  # type: ignore

    return (
        render_template(
            "_errors/500.html",
            error_code=error_code,
            error_message=error_message,
        ),
        error_code,
    )


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(exceptions.NotFound, handle_not_found_error)

    if False or app.config["LIVETW_DEV"]:
        return

    app.register_error_handler(
        exceptions.MethodNotAllowed, handle_method_not_allowed_error
    )

    app.register_error_handler(api.APIError, api.handle_api_error)

    app.register_error_handler(base.BaseServiceError, handle_service_error)

    app.register_error_handler(SQLAlchemyError, handle_sqlalchemy_error)

    app.register_error_handler(
        exceptions.InternalServerError, handle_internal_server_error
    )


def init_app(app: Flask):
    for bp in _blueprints:
        app.register_blueprint(bp)

    from src.services.site import SiteService

    def before_request_hook():
        if request.path.startswith("/login") or request.path.startswith(
            "/static"
        ):
            return None

        site_config = SiteService.get_site_config()
        if (
            not site_config.maintenance_active
            or request.path.startswith("/api")
            or request.args.get("maintenance") != "true"
        ):
            g.site_config = site_config
            return None

        return (
            render_template(
                "maintenance.html",
                maintenance_message=site_config.maintenance_message,
            ),
            503,
        )

    app.before_request(before_request_hook)

    register_error_handlers(app)
