import dataclasses
import typing as t
from datetime import datetime

from sqlalchemy import DateTime, String, orm, sql
from typing_extensions import Annotated

OptionalTuple = t.Union[t.Tuple[str, ...], None]


def _empty_str_tuple() -> t.Tuple[str, ...]:
    return tuple()


class BaseModel(orm.DeclarativeBase, orm.MappedAsDataclass):
    def _hidden_columns(self) -> OptionalTuple:
        return None

    def asdict(
        self, keys: OptionalTuple = None, exclude: bool = False
    ) -> t.Dict[str, t.Any]:
        mapped_dict = dataclasses.asdict(self)

        hidden_keys = self._hidden_columns() or _empty_str_tuple()
        if exclude:
            exclude_keys = hidden_keys + (keys or _empty_str_tuple())
            return {
                key: mapped_dict[key]
                for key in mapped_dict.keys()
                if key not in exclude_keys
            }

        for key in hidden_keys:
            mapped_dict.pop(key, None)

        if keys:
            return {key: mapped_dict[key] for key in keys}

        return mapped_dict


IntPK = Annotated[int, orm.mapped_column(primary_key=True)]

Timestamp = Annotated[
    datetime, orm.mapped_column(server_default=sql.func.current_timestamp())
]
CreatedAt = Annotated[
    datetime,
    orm.mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    ),
]
UpdatedAt = Annotated[
    datetime,
    orm.mapped_column(
        server_default=sql.func.current_timestamp(),
        onupdate=datetime.utcnow,
    ),
]

Str32 = Annotated[str, orm.mapped_column(String(32))]
Str256 = Annotated[str, orm.mapped_column(String(256))]
Str512 = Annotated[str, orm.mapped_column(String(512))]
