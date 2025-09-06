from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base
import enum


class CategoryLevel(enum.Enum):
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"


class Category(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("Categories.id", ondelete="CASCADE"), nullable=True
    )

    image_url: Mapped[str | None] = mapped_column(String, nullable=True)

    children: Mapped[list["Category"]] = relationship(
        "Category", back_populates="parent"
    )

    parent: Mapped["Category"] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children",
    )

    product_categories: Mapped[list["ProductCategory"]] = relationship(  # type: ignore
        "ProductCategory", back_populates="category"
    )

    __table_args__ = (
        UniqueConstraint("name", name="uq_category_name"),
        Index("ix_category_parent_id", "parent_id"),
    )
