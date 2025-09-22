from logging import error
from typing import List, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Product



class CartRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_cart(self, product_ids: List[int]) -> Dict:
        stmt = select(
            Product.id,
            Product.name,
            Product.main_image,
            Product.base_price,
            Product.discount_percentage,
        ).where(Product.id.in_(product_ids))

        try:
            result = await self.session.execute(stmt)
            rows = result.mappings().all()

            return rows

        except Exception as e:
            error(f"Error fetching cart items: {e}")
            return None
