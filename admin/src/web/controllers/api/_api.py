import typing as t
from functools import wraps

from flask import request
from flask import typing as tf
from flask_wtf import FlaskForm  # pyright: ignore[reportMissingTypeStubs]

from src.utils import status

API_ERROR_RESPONSE = (
    {"message": "Parametros invalidos"},
    status.HTTP_400_BAD_REQUEST,
)

TRoute = t.TypeVar("TRoute", bound=t.Callable[..., t.Any])


def validation(
    schema: t.Type[FlaskForm],
    content_type: t.Union[t.Literal["json"], t.Literal[False]] = "json",
) -> t.Callable[[TRoute], TRoute]:
    def decorator(func: TRoute) -> TRoute:
        @wraps(func)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> tf.ResponseReturnValue:
            if content_type == "json" and not request.is_json:
                return API_ERROR_RESPONSE

            form = schema(csrf_enabled=False)

            if not form.validate():
                return API_ERROR_RESPONSE

            return func(
                form.values(),  # pyright: ignore[reportGeneralTypeIssues]
                *args,
                **kwargs
            )

        return t.cast(TRoute, wrapper)

    return decorator


# class APIError(Exception):
#     def __init__(self, message: str, status_code: int = 400):
#         super().__init__(message)
#         self.message = message
#         self.status_code = status_code

#     def asdict(self):
#         rv: t.Dict[str, t.Union[t.Dict[str, t.Any], str, int]] = dict()
#         rv["message"] = self.message
#         return rv
