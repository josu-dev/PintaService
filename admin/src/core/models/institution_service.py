from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.models.base import BaseModel, IntPK, Timestamp


class InstitutionService(BaseModel):
    __tablename__ = "institution_service"

    id: Mapped[IntPK] = mapped_column(init=False)

    service_id = Column(Integer, ForeignKey("services.id"))
    institution_id = Column(Integer, ForeignKey("institutions.id"))

    created_at: Mapped[Timestamp] = mapped_column(init=False)
    updated_at: Mapped[Timestamp] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
