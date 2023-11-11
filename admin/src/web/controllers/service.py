from flask import Blueprint, g, redirect, render_template, request

from src.services.service import ServiceService
from src.utils import status
from src.web.controllers import _helpers as h
from src.web.forms.service import ServiceForm

bp = Blueprint("services", __name__)


@bp.get("/")
@h.authenticated_route(module="services", permissions=("index",))
def services_get(institution_id: int):
    page, per_page = h.url_pagination_args(
        default_per_page=g.site_config.page_size
    )

    services, total = ServiceService.get_institution_services_paginated(
        institution_id, page, per_page
    )

    return render_template(
        "institutions/[id]/services/index.html",
        services=services,
        page=page,
        per_page=per_page,
        total=total,
    )


@bp.get("/new")
@h.authenticated_route(module="services", permissions=("create",))
def services_new_get(institution_id: int):
    form = ServiceForm()

    return render_template("institutions/[id]/services/new.html", form=form)


@bp.post("/new")
@h.authenticated_route(module="services", permissions=("create",))
def services_new_post(institution_id: int):
    form = ServiceForm()
    if not form.validate():
        return (
            render_template("institutions/[id]/services/new.html", form=form),
            status.HTTP_400_BAD_REQUEST,
        )

    try:
        service = ServiceService.create_service(
            institution_id, **form.values()
        )
    except ServiceService.ServiceServiceError as e:
        h.flash_error(e.message)
        return (
            render_template("institutions/[id]/services/new.html", form=form),
            status.HTTP_400_BAD_REQUEST,
        )

    h.flash_success("Servicio creado exitosamente")
    return redirect(f"/institutions/{institution_id}/services/{service.id}")


@bp.get("/<int:service_id>")
@h.authenticated_route(module="services", permissions=("show", "update"))
def services_id_get(institution_id: int, service_id: int):
    service = ServiceService.get_service(service_id)
    if not service:
        h.flash_info(f"Servicio '{service_id}' no encontrado")
        return redirect(f"/institutions/{institution_id}/services")

    form = ServiceForm(obj=service)

    return render_template(
        "institutions/[id]/services/update.html",
        form=form,
    )


@bp.post("/<int:service_id>")
@h.authenticated_route(module="services", permissions=("update",))
def services_id_post(institution_id: int, service_id: int):
    service = ServiceService.get_service(service_id)
    if not service:
        h.flash_info(
            f"Servicio con id '{service_id}' no encontrado al actualizar"
        )
        return redirect(f"/institutions/{institution_id}/services")

    form = ServiceForm(request.form)
    if not form.validate():
        return (
            render_template(
                "institutions/[id]/services/update.html",
                form=form,
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    try:
        result = ServiceService.update_service(service_id, **form.values())
    except ServiceService.ServiceServiceError:
        h.flash_info("No se pudo actualizar el servicio")
        return (
            render_template(
                "institutions/[id]/services/update.html",
                form=form,
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not result:
        h.flash_info("No se pudo actualizar el servicio")
    else:
        h.flash_success("Servicio actualizado exitosamente")

    return render_template(
        "institutions/[id]/services/update.html",
        form=form,
    )


@bp.post("/<int:service_id>/delete")
@h.authenticated_route(module="services", permissions=("destroy",))
def services_id_delete(institution_id: int, service_id: int):
    service = ServiceService.get_service(service_id)
    if not service:
        h.flash_info(
            f"Servicio con id '{service_id}' no encontrado al eliminar"
        )
        return redirect(f"/institutions/{institution_id}/services")

    result = ServiceService.delete_service(service_id)
    if result:
        h.flash_success("Servicio eliminado exitosamente")
        return redirect(f"/institutions/{institution_id}/services")

    h.flash_error("No se pudo eliminar el servicio")
    return redirect(f"/institutions/{institution_id}/services")
