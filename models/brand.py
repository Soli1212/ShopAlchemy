from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base

from .product import Product


class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    image_url: Mapped[str] = mapped_column(String(200), nullable=True)

    description: Mapped[str] = mapped_column(String, nullable=True)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="brand")

    __table_args__ = (
        UniqueConstraint("name", name="uq_brand_name"),
    )