from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class ProductTag(Base):
    __tablename__ = "product_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tags.id"), nullable=False)

    product = relationship("Product", back_populates="product_tags")
    tag = relationship("Tag", back_populates="product_tags")

    __table_args__ = (
        UniqueConstraint("product_id", "tag_id", name="uq_product_tag_combo"),
        Index("ix_producttag_product_id", "product_id"),
        Index("ix_producttag_tag_id", "tag_id"),
    )
