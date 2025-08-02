from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import Index, UniqueConstraint

from connection import Base


class VariantOption(Base):
    __tablename__ = "variant_options"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str | None] = mapped_column(String(100))

    __table_args__ = (
        UniqueConstraint("name", name="unique_variant_option_name"),
        Index("idx_variant_options_name", "name"),
    )
