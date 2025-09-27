from logging import error
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, load_only, contains_eager
from sqlalchemy.exc import SQLAlchemyError

from models import ProductVariant, Product, VariantConfig, VariantOption

class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cart(self, variant_ids: List[str]) -> List[Dict[str, Any]]:
        stmt = (
            select(ProductVariant)
            .join(Product)
            .join(VariantConfig)
            .join(VariantOption)
            .options(
                contains_eager(ProductVariant.product).load_only(
                    Product.id,
                    Product.name,
                    Product.base_price,
                    Product.discount_percentage,
                    Product.main_image,
                    Product.created_at,
                ),
                contains_eager(ProductVariant.config).load_only(
                    VariantConfig.option_id,
                    VariantConfig.value
                )
                .contains_eager(VariantConfig.option).load_only(
                    VariantOption.name,
                    VariantOption.label
                )
            )
            .where(ProductVariant.id.in_(variant_ids), ProductVariant.is_active == True)
        )

        try:
            result = await self.session.execute(stmt)
            rows = result.unique().scalars().all()
            return rows
        except Exception as e:
            error(f"Error fetching cart items: {e}")
            return None