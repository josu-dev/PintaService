from flask import Flask, g, render_template, request
from werkzeug import exceptions

from src.web.controllers import admin, api, root

_blueprints = (
    admin.bp,
    api.bp,
    root.bp,
)


def handle_not_found_error(e: exceptions.NotFound):
    if request.path.startswith("/api"):
        return api.API_NOT_FOUND_RESPONSE

    return (
        render_template(
            "error.html",
            error_code="404",
            error_message="Página no encontrada",
        ),
        404,
    )


def handle_method_not_allowed_error(e: exceptions.MethodNotAllowed):
    if request.path.startswith("/api"):
        return api.API_METHOD_NOT_ALLOWED_RESPONSE

    return (
        render_template(
            "error.html",
            error_code="405",
            error_message=f"Método {request.method} no permitido",
        ),
        405,
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

    app.register_error_handler(exceptions.NotFound, handle_not_found_error)

    app.register_error_handler(
        exceptions.MethodNotAllowed, handle_method_not_allowed_error
    )

    app.register_error_handler(api.APIError, api.handle_api_error)
