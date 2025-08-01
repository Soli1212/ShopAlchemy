import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_phone_number", "phone_number", unique=True),
        Index("ix_users_created_at", "created_at"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )

    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    phone_number: Mapped[str] = mapped_column(String(11), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    discounts: Mapped[list["Discount"]] = relationship("Discount", back_populates="user")  # type: ignore
    addresses: Mapped[list["UserAddress"]] = relationship("UserAddress", back_populates="user")  # type: ignore
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")  # type: ignore
