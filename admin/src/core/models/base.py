from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, mapped_column
from sqlalchemy.sql import func
from typing_extensions import Annotated


class BaseModel(DeclarativeBase, MappedAsDataclass):
    pass


IntPK = Annotated[int, mapped_column(primary_key=True)]

Timestamp = Annotated[
    datetime, mapped_column(server_default=func.current_timestamp())
]
CreatedAt = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    ),
]
UpdatedAt = Annotated[
    datetime,
    mapped_column(
        server_default=func.current_timestamp(),
        onupdate=datetime.utcnow,
    ),
]

Str32 = Annotated[str, mapped_column(String(32))]
Str256 = Annotated[str, mapped_column(String(256))]
Str512 = Annotated[str, mapped_column(String(512))]
