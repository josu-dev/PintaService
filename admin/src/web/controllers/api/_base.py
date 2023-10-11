import dataclasses
import typing as t
from functools import wraps

from flask import request
from flask import typing as tf
from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]

from src.utils import status

API_BAD_REQUEST_RESPONSE = (
    {"message": "Parametros invalidos"},
    status.HTTP_400_BAD_REQUEST,
)

API_NOT_FOUND_RESPONSE = (
    {"message": "Endpoint invalido"},
    status.HTTP_404_NOT_FOUND,
)

API_METHOD_NOT_ALLOWED_RESPONSE = (
    {"message": "Metodo no permitido"},
    status.HTTP_405_METHOD_NOT_ALLOWED,
)

API_INTERNAL_SERVER_ERROR_RESPONSE = (
    {"message": "Error interno del servidor"},
    status.HTTP_500_INTERNAL_SERVER_ERROR,
)


@dataclasses.dataclass
class APIError(Exception):
    message: str
    status_code: int


TRoute = t.TypeVar("TRoute", bound=t.Callable[..., t.Any])


def validation(
    schema: t.Type[FlaskForm],
    method: t.Literal["GET", "POST"] = "POST",
    content_type: t.Literal["json", False] = "json",
    debug: bool = False,
) -> t.Callable[[TRoute], TRoute]:
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if content_type == "json" and not request.is_json:
                return API_BAD_REQUEST_RESPONSE

            if method == "GET":
                form = schema(request.args, csrf_enabled=False)
                res_kwarg = "args"
            else:
                form = schema(csrf_enabled=False)
                res_kwarg = "body"

            if not form.validate():
                if debug:
                    print(form.errors, flush=True)  # pyright: ignore
                return API_BAD_REQUEST_RESPONSE

            kwargs[res_kwarg] = form.values()  # pyright: ignore

            return func(*args, **kwargs)

        return t.cast(TRoute, wrapper)

    return decorator
