import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.core.enums import ServiceTypes
from src.core.models.base import (
    BaseModel,
    CreatedAt,
    IntPK,
    Str32,
    Str256,
    Str512,
    UpdatedAt,
)
from src.core.models.search import TSVectorType


class Service(BaseModel):
    __tablename__ = "services"

    id: Mapped[IntPK] = mapped_column(init=False)
    name: Mapped[Str32]
    laboratory: Mapped[Str32]
    description: Mapped[Str512]
    keywords: Mapped[Str256]
    service_type: Mapped[ServiceTypes]

    institution_id: Mapped[int]

    created_at: Mapped[CreatedAt] = mapped_column(init=False)
    updated_at: Mapped[UpdatedAt] = mapped_column(
        init=False, onupdate=func.current_timestamp()
    )

    enabled: Mapped[bool] = mapped_column(default=True)

    search_tsv = sa.Column(  # pyright: ignore[reportUnknownVariableType]
        TSVectorType(
            "name",
            "laboratory",
            "description",
            "keywords",
            regconfig="argentino",
        ),
        sa.Computed(
            "to_tsvector('argentino', \"name\" || ' ' || \"laboratory\" || ' ' || \"description\" || ' ' || \"keywords\")",  # noqa E501
            persisted=True,
        ),
    )
    #   equivalent to:
    #   COLUMN search_tsv TSVECTOR GENERATED ALWAYS AS (
    #       to_tsvector(
    #           'argentino',
    #           "name" || ' ' || "laboratory" || ' ' || "description" || ' ' || "keywords" # noqa E501
    #       )
    #   ) STORED;

    __table_args__ = (
        # Indexing the TSVector column
        sa.Index(
            "idx_service_search_tsv",
            search_tsv,  # pyright: ignore[reportUnknownArgumentType]
            postgresql_using="gin",
        ),
    )
