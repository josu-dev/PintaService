import typing as t
from functools import wraps

from flask import request
from flask import typing as tf
from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]

from src.utils import status

API_BAD_REQUEST_RESPONSE = (
    {"error": "Parametros invalidos"},
    status.HTTP_400_BAD_REQUEST,
)

API_UNAUTHORIZED_RESPONSE = (
    {"error": "No autorizado"},
    status.HTTP_401_UNAUTHORIZED,
)

API_NOT_FOUND_RESPONSE = (
    {"error": "Endpoint invalido"},
    status.HTTP_404_NOT_FOUND,
)

API_METHOD_NOT_ALLOWED_RESPONSE = (
    {"error": "Metodo no permitido"},
    status.HTTP_405_METHOD_NOT_ALLOWED,
)

API_INTERNAL_SERVER_ERROR_RESPONSE = (
    {"error": "Error interno del servidor"},
    status.HTTP_500_INTERNAL_SERVER_ERROR,
)


class BaseAPIError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str,
        status_code: t.Union[int, None] = None,
        payload: t.Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def asdict(self) -> t.Dict[str, t.Any]:
        rv = dict(self.payload or ())
        rv["error"] = self.message
        return rv


TRoute = t.TypeVar("TRoute", bound=t.Callable[..., t.Any])


def validation(
    schema: t.Type[FlaskForm],
    method: t.Literal["GET", "POST"] = "POST",
    content_type: t.Literal["json", False] = "json",
    auth_required: bool = False,
    debug: bool = False,
) -> t.Callable[[TRoute], TRoute]:
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if content_type == "json" and not request.is_json:
                return API_BAD_REQUEST_RESPONSE

            if auth_required:
                # TODO: implement jwt auth
                # if not authorized: return API_UNAUTHORIZED_RESPONSE
                ...

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
