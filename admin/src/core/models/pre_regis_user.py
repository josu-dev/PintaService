from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.models.base import (
    BaseModel,
    IntPK,
    Str32,
    Str64,
    Str128,
    Timestamp,
)


class PreRegisterUser(BaseModel):
    __tablename__ = "PreRegisterUsers"

    id: Mapped[IntPK] = mapped_column(init=False)
    firstname: Mapped[Str32]
    lastname: Mapped[Str32]
    email: Mapped[Str64]
    token: Mapped[Str128]

    created_at: Mapped[Timestamp] = mapped_column(init=False)
    updated_at: Mapped[Timestamp] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
