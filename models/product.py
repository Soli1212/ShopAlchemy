import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DECIMAL,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        Index("ix_products_name", "name", unique=True),
        Index("ix_products_brand_id", "brand_id"),
        Index("ix_products_new", "new"),
        Index("ix_products_lux", "lux"),
        Index("ix_products_suggested", "suggested"),
        Index("ix_products_trend", "trend"),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    brand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("brands.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    base_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    main_image: Mapped[str] = mapped_column(String(200), nullable=False)

    new: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    lux: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    suggested: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    trend: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    product_categories: Mapped[list["ProductCategory"]] = relationship(  # type: ignore
        "ProductCategory", back_populates="product"
    )
    product_tags: Mapped[list["ProductTag"]] = relationship(  # type: ignore
        "ProductTag", back_populates="product"
    )
    product_attributes: Mapped[list["ProductAttribute"]] = relationship(  # type: ignore
        "ProductAttribute", back_populates="product"
    )
    variants: Mapped[list["ProductVariant"]] = relationship(  # type: ignore
        "ProductVariant", back_populates="product"
    )
    brand: Mapped["Brand"] = relationship("Brand", back_populates="products")  # type: ignore
