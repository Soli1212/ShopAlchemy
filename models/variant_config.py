from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from connection import Base


class VariantConfig(Base):
    __tablename__ = "variant_configs"

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("product_variants.id"), nullable=False
    )
    option_id: Mapped[int] = mapped_column(
        ForeignKey("variant_options.id"), nullable=False
    )
    value: Mapped[str] = mapped_column(String(100), nullable=False)

    variant: Mapped["ProductVariant"] = relationship("ProductVariant", back_populates="config")  # type: ignore
    option: Mapped["VariantOption"] = relationship("VariantOption")  # type: ignore

    __table_args__ = (
        UniqueConstraint("variant_id", "option_id", name="unique_variant_config"),
        Index("idx_variant_configs_variant_option", "variant_id", "option_id"),
    )
