import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base

from .order_item import OrderItem
from .user import User
from .user_address import UserAddress


class OrderStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    canceled = "canceled"
    expired = "expired"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index("ix_orders_transaction_id", "transaction_id", unique=True),
        Index("ix_orders_status", "status"),
        Index("ix_orders_created_at", "created_at"),
        Index("ix_orders_user_id_status", "user_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    status: Mapped[OrderStatus] = mapped_column(
        SqlEnum(OrderStatus), default=OrderStatus.pending
    )

    discount_id: Mapped[int | None] = mapped_column(
        ForeignKey("discounts.id", ondelete="SET NULL"), nullable=True
    )

    address_id: Mapped[int | None] = mapped_column(
        ForeignKey("user_addresses.id", ondelete="SET NULL"), nullable=True
    )

    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(8, 2))
    discount_amount: Mapped[Decimal | None] = mapped_column(
        DECIMAL(8, 2), nullable=True
    )
    final_amount: Mapped[Decimal] = mapped_column(DECIMAL(8, 2))

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    payment_gateway: Mapped[str | None] = mapped_column(String(50), nullable=True)
    transaction_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    paid_at: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    address: Mapped["UserAddress"] = relationship("address", back_populates="orders")