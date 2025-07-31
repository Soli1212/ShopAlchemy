from datetime import datetime

from sqlalchemy import (Boolean, DateTime, ForeignKey, Index, Integer, Numeric,
                        String, UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base

from .user import User


class Discount(Base):
    __tablename__ = "discounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    min_order_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    max_order_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    use_limit: Mapped[int] = mapped_column(Integer, nullable=True)
    min_order_count: Mapped[int] = mapped_column(Integer, nullable=True)
    used_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="SET DEFAULT", onupdate="CASCADE"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="discounts")

    __table_args__ = (
        UniqueConstraint("code", name="uq_discount_code"),
        Index("ix_discount_start_end", "start_date", "end_date"),
        Index("ix_discount_user_id", "user_id"),
    )