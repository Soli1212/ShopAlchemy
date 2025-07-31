from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    product_tags: Mapped[list["ProductTag"]] = relationship("ProductTag", back_populates="tag")  # type: ignore

    __table_args__ = (
        UniqueConstraint("name", name="uq_tag_name"),
    )