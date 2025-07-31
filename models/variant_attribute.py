from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class VariantAttribute(Base):
    __tablename__ = "variant_attributes"

    id: Mapped[int] = mapped_column(primary_key=True)

    variant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("product_variants.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    attribute_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("attributes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    value: Mapped[str] = mapped_column(String(100), nullable=False)

    variant: Mapped["ProductVariant"] = relationship(  # type: ignore
        "ProductVariant", back_populates="attributes"
    )

    attribute: Mapped["Attribute"] = relationship("Attribute")  # type: ignore

    __table_args__ = (
        Index("ix_variant_attribute_variant_id", "variant_id"),
        Index("ix_variant_attribute_attribute_id", "attribute_id"),
        # Index("ix_variant_attribute_pair", "variant_id", "attribute_id"),
        UniqueConstraint("variant_id", "attribute_id", name="uq_variant_attr_combo"),
    )
