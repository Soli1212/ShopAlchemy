from logging import error
from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import ProductVariant, Product



class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cart(self, product_ids: List[int]) -> Dict:
        stmt = (
            select(
                Product.id,
                Product.name,
                Product.base_price,
                Product.discount_percentage,
                Product.main_image,
            )   
            .join(ProductVariant, ProductVariant.product_id == Product.id)
            .where(ProductVariant.id.in_(product_ids))
        )

        try:
            result = await self.session.execute(stmt)
            rows = result.mappings().all()

            return rows

        except Exception as e:
            error(f"Error fetching cart items: {e}")
            return None
