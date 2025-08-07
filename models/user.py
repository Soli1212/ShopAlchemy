import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from connection import Base


class Gender(enum.Enum):
    female = "female"
    male = "male"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("ix_users_phone_number", "phone_number"),
        Index("ix_users_created_at", "created_at"),
        UniqueConstraint("phone_number", name="uq_users_phone_number"),
        UniqueConstraint("email", name="uq_users_email"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(11), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    gender: Mapped[Gender | None] = mapped_column(SqlEnum(Gender), nullable=True)
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
