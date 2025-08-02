import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, Boolean, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base

from .product import Product
from .variant_config import VariantConfig
from .variant_image import VariantImage


class ProductVariant(Base):
    __tablename__ = "product_variants"
    __table_args__ = (
        Index("ix_product_variants_product_id", "product_id"),
        Index("ix_product_variants_sku", "sku", unique=True),
        Index("ix_product_variants_stock", "stock"),
        Index("ix_product_variants_is_active", "is_active"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    price_override: Mapped[Decimal | None] = mapped_column(DECIMAL(8, 2), nullable=True)
    discount_percentage: Mapped[int | None] = mapped_column(Integer, nullable=True)

    sku: Mapped[str] = mapped_column(String(100), nullable=False)

    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    product: Mapped["Product"] = relationship("Product", back_populates="variants")

    images: Mapped[list["VariantImage"]] = relationship(
        "VariantImage", back_populates="variant"
    )

    config: Mapped[list["VariantConfig"]] = relationship(
        "VariantConfig", back_populates="variant"
    )
