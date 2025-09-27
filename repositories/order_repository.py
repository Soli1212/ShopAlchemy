from logging import error
from typing import Dict, Optional, List
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, Session

from models import Order, OrderItem, OrderStatus

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def checkout(
        self,
        user_id: str,
        discount_id: Optional[int],
        address_id: int,
        total_amount: Decimal,
        discount_amount: Optional[Decimal],
        final_amount: Decimal,
        item_mappings: List[Dict],
        description: Optional[str] = None,
        status: OrderStatus = OrderStatus.pending,
    ) -> Optional[Order]:
        try:
            order = Order(
                user_id=user_id,
                discount_id=discount_id,
                address_id=address_id,
                total_amount=total_amount,
                discount_amount=discount_amount,
                final_amount=final_amount,
                description=description,
                status=status,
            )
            self.session.add(order)
            await self.session.flush()

            for i in item_mappings: i["order_id"] = order.id

            await self.session.run_sync(
                lambda sync_session: sync_session.bulk_insert_mappings(
                    OrderItem, item_mappings
                )
            )

            result = await self.session.execute(
                select(Order).options(selectinload(Order.items)).filter_by(id=order.id)
            )
            order = result.scalars().first()

            return True

        except Exception as e:
            await self.session.rollback()
            error(f"Error creating order: {e}")
            return None

    async def set_order_status(order_id: str, status: OrderStatus):
        ...
    
    async def get_user_orders(self, user_id: str) -> List[Order]:
        ...
    
    async def get_order_by_id(self, order_id: str) -> Optional[Order]:
        ... 
    
