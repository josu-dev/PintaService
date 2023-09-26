from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import BaseModel, IntPK


class Association(BaseModel):
    __tablename__ = "association"
    user_id: Mapped[IntPK] = mapped_column(ForeignKey("users.id"), init=False)
    institution_id: Mapped[IntPK] = mapped_column(
        ForeignKey("institutions.id"), init=False
    )
