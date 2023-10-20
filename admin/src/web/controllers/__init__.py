import typing as t

import flask

from src.web.controllers import admin, api, institution, request, root, service

service.bp.register_blueprint(
    request.bp, url_prefix="/<int:service_id>/requests"
)
institution.bp.register_blueprint(
    service.bp, url_prefix="/<int:institution_id>/services"
)

_blueprints = (
    admin.bp,
    api.bp,
    root.bp,
    institution.bp,
)


def init_app(app: flask.Flask):
    from src.web.controllers import _errors

    _errors.register_error_handlers(app)

    for bp in _blueprints:
        app.register_blueprint(bp)

    from src.services.auth import AuthService
    from src.services.institution import InstitutionService
    from src.services.site import SiteService
    from src.services.user import UserService

    def user_has_permissions(_: t.Tuple[str, ...]) -> bool:
        return False

    def get_institution_id(url_path: str) -> t.Union[int, None]:
        if not url_path.startswith("/institutions/"):
            return None

        institution_id = url_path.split("/")[2]
        if institution_id.isdigit():
            return int(institution_id)

        return None

    def before_request_hook():
        if flask.request.path.startswith("/static"):
            return None

        flask.g.user = None
        flask.g.user_permissions = tuple()
        flask.g.user_has_permissions = user_has_permissions
        flask.g.institution_id = None
        flask.g.institutions = tuple()

        user_id = flask.session.get("user_id")  # type: ignore
        if user_id is not None:
            user = UserService.get_user(user_id)  # type: ignore
            if user is None:
                flask.session.clear()
            else:
                flask.g.user = user

                if flask.session.get("is_admin"):
                    flask.g.user_permissions = (
                        AuthService.get_site_admin_permissions(user.id)
                    )
                    flask.g.institutions = (
                        InstitutionService.get_all_institutions()
                    )
                else:
                    institution_id = get_institution_id(flask.request.path)
                    flask.g.instituin_id = institution_id

                    if institution_id is not None:
                        flask.g.user_permissions = (
                            AuthService.get_user_permissions(
                                user.id, institution_id
                            )
                        )
                    flask.g.institutions = (
                        InstitutionService.get_user_institutions(user.id)
                    )

        site_config = SiteService.get_site_config()
        flask.g.site_config = site_config

        if (
            not site_config.maintenance_active
            or ("setting_update" in flask.g.user_permissions)
            or flask.request.path.startswith("/login")
        ):
            return None

        return (
            flask.render_template(
                "maintenance.html",
                maintenance_message=site_config.maintenance_message,
            ),
            503,
        )

    app.before_request(before_request_hook)

    @app.context_processor
    def inject_template_variables() -> t.Dict[str, t.Any]:
        if flask.request.view_args is None:
            return {}

        res = {
            f"param_{key}": value
            for key, value in flask.request.view_args.items()
        }
        return res
