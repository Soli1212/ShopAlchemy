import uuid

from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class VariantImage(Base):
    __tablename__ = "variant_images"

    __table_args__ = (
        Index("ix_variant_images_variant_id", "variant_id"),
        Index(
            "uq_variant_images_variant_image", "variant_id", "image_url", unique=True
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    variant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("product_variants.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    image_url: Mapped[str] = mapped_column(String(200), nullable=False)

    alt_text: Mapped[str | None] = mapped_column(String(100), nullable=True)

    variant: Mapped["ProductVariant"] = relationship(  # type: ignore
        "ProductVariant", back_populates="images"
    )
