from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import Optional
from models import Discount



class DiscountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_discount(self, discount_id: int) -> Optional[dict]:
        query = select(Discount).where(Discount.Discount.id == discount_id)
        result = await self.session.execute(query)
        return result.mappings().first()
        
    async def update_used_count(self, discount_id: int, used_count: int = 1) -> None:
        query = (
            update(Discount)
            .where(Discount.id == discount_id)
            .values(used_count=Discount.used_count + used_count)
        )
        await self.session.execute(query)

    async def change_discount_activity(self, discount_id: int, is_active: bool) -> None:
        query = (
            update(Discount)
            .where(Discount.id == discount_id)
            .values({"is_active": is_active})
        )
        await self.session.execute(query)

    
