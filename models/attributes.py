from sqlalchemy import Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class Attribute(Base):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    name: Mapped[str] = mapped_column(String(250), nullable=False)

    label: Mapped[str | None] = mapped_column(String(100), nullable=True)

    product_attributes: Mapped[list["ProductAttribute"]] = relationship(  # type: ignore
        "ProductAttribute", back_populates="attribute"
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_attribute_name"),
        UniqueConstraint("label", name="uq_attribute_label"),
    )
