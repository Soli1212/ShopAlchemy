from sqlalchemy import (BigInteger, ForeignKey, Index, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base

from .category import Category
from .product import Product


class ProductCategory(Base):
    __tablename__ = "ProductCategories"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)

    product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Categories.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        "Product", back_populates="product_categories"
    )
    category: Mapped["Category"] = relationship(
        "Category", back_populates="product_categories"
    )

    __table_args__ = (
        UniqueConstraint("product_id", "category_id", name="uq_product_category"),
        Index("ix_product_id", "product_id"),
        Index("ix_category_id", "category_id"),
    )
