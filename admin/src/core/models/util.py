import dataclasses
import datetime
import decimal
import typing as t
import uuid

from werkzeug.http import http_date

if t.TYPE_CHECKING:
    from src.core.models.base import BaseModel


def _sanitize_value(o: t.Any) -> t.Any:
    if isinstance(o, datetime.date):
        return http_date(o)

    if isinstance(o, (decimal.Decimal, uuid.UUID)):
        return str(o)

    if dataclasses and dataclasses.is_dataclass(o):
        return dataclasses.asdict(o)

    return o


def jsoneable(
    model: BaseModel,
    keys: t.Union[t.Tuple[str, ...], str, None] = None,
    exclude: bool = False,
) -> t.Dict[str, t.Any]:
    keys = (keys,) if isinstance(keys, str) else keys or ()

    if exclude:
        return {
            key: _sanitize_value(value)
            for key, value in dataclasses.asdict(model).items()
            if key in keys
        }

    return {
        key: _sanitize_value(value)
        for key, value in dataclasses.asdict(model).items()
        if key not in keys
    }


def model_as_dict(
    model: BaseModel,
    keys: t.Union[t.Tuple[str, ...], str, None] = None,
    exclude: bool = False,
) -> t.Dict[str, t.Any]:
    keys = (keys,) if isinstance(keys, str) else keys or ()

    if exclude:
        return {
            key: value
            for key, value in dataclasses.asdict(model).items()
            if key not in keys
        }

    return {
        key: value
        for key, value in dataclasses.asdict(model).items()
        if key in keys
    }
