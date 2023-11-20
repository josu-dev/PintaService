import functools
import typing as t

import flask
import flask_wtf
from flask import typing as tf
from flask_jwt_extended import view_decorators

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
    """Base API error class.

    An API error is an exception that is raised when an API endpoint
    fails to execute its business logic.

    Attributes:
        message: A human-readable message describing the error.
        status_code: The HTTP status code to return.
        payload: A dictionary containing additional information related
            to the error.
    """

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


def handle_api_error(e: BaseAPIError):
    return (
        e.asdict(),
        e.status_code,
    )


TRoute = t.TypeVar("TRoute", bound=t.Callable[..., t.Any])


def validation(
    schema: t.Optional[t.Type[flask_wtf.FlaskForm]] = None,
    method: t.Literal["GET", "POST"] = "POST",
    content_type: t.Literal["json", False] = "json",
    require_auth: bool = False,
    debug: bool = False,
) -> t.Callable[[TRoute], TRoute]:
    _content_type = False if method == "GET" else content_type

    def decorator(func: TRoute) -> TRoute:
        @functools.wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if _content_type == "json" and not flask.request.is_json:
                return API_BAD_REQUEST_RESPONSE

            if require_auth:
                view_decorators.verify_jwt_in_request()

            if schema is not None:
                if method == "GET":
                    form = schema(flask.request.args, meta={"csrf": False})
                    form_arg = "args"
                else:
                    form = schema(meta={"csrf": False})
                    form_arg = "body"

                if not form.validate():
                    if debug:
                        print(form.errors, flush=True)
                    return API_BAD_REQUEST_RESPONSE

                kwargs[form_arg] = form.values()  # pyright: ignore

            return func(*args, **kwargs)

        return wrapper  # pyright: ignore[reportGeneralTypeIssues]

    return decorator
