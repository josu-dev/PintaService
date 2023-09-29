from typing import List

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.core.models.base import BaseModel, IntPK, Timestamp
from src.core.models.institution import Institution
from src.core.models.service import Service


class Institution_Service(BaseModel):
    __tablename__ = "institution_service"

    id: Mapped[IntPK] = mapped_column(init=False)
    service_id = Column(Integer, ForeignKey("services.id"))
    institution_id = Column(Integer, ForeignKey("institutions.id"))

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
