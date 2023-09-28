from typing import List

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import BaseModel, IntPK
from src.core.models.institution import Institution
from src.core.models.user import User


class InstitutionUser(BaseModel):
    __tablename__ = "institution_user"

    id: Mapped[IntPK] = mapped_column(init=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    institution_id = Column(Integer, ForeignKey("institutions.id"))

    # Relation Between user and institution
    user: Mapped[List[User]] = relationship(
        "User", back_populates="institutions"
    )
    institution: Mapped[List[Institution]] = relationship(
        "Institution", back_populates="users"
    )
