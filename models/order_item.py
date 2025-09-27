from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        Index("ix_order_items_order_id", "order_id"),
        Index("ix_order_items_product_id", "product_id"),
        Index("ix_order_items_variant_id", "variant_id"),
        # Index("ix_order_items_order_product", "order_id", "product_id"),  # Optional, for specific queries
    )

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)

    order_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("orders.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    product_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("products.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    variant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("product_variants.id", ondelete="SET NULL", onupdate="CASCADE"),
    )

    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    product_unit_price: Mapped[Decimal] = mapped_column(DECIMAL(8, 2), nullable=False)
    variant_price_override: Mapped[Decimal] = mapped_column(DECIMAL(8, 2), nullable=False)
    discounted_price: Mapped[Decimal | None] = mapped_column(
        DECIMAL(8, 2), nullable=True
    )
    total_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")  # type: ignore
