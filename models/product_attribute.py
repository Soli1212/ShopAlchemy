from sqlalchemy import (BigInteger, ForeignKey, Index, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base
from models.attributes import Attribute


class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)

    product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    attribute_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("attributes.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    default_value: Mapped[str] = mapped_column(String(100))

    product = relationship("Product", back_populates="product_attributes")

    attribute: Mapped["Attribute"] = relationship(
        "Attribute", back_populates="product_attributes"
    )

    __table_args__ = (
        Index("ix_product_attribute_product_id", "product_id"),
        Index("ix_product_attribute_attribute_id", "attribute_id"),
        # Index("ix_product_attribute_pair", "product_id", "attribute_id"),
        UniqueConstraint("product_id", "attribute_id", name="uq_product_attr_combo"),
    )
