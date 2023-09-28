from typing import List

from core.models.base import BaseModel, IntPK, Timestamp
from core.models.institution import Institution
from core.models.service import Service
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Institution_Service(BaseModel):
    __tablename__ = "institution_service"

    id: Mapped[IntPK] = mapped_column(init=False)
    institution_id: int
    service_id: int

    service: Mapped[List[Service]] = relationship(
        "Service", back_populates="institutions"
    )
    institution: Mapped[List[Institution]] = relationship(
        "Institution", back_populates="services"
    )

    created_at: Mapped[Timestamp] = mapped_column(init=False)
    updated_at: Mapped[Timestamp] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )
