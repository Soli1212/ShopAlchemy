from decimal import Decimal
from logging import error
from typing import Dict, List, Optional

from sqlalchemy import update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, load_only

from models import Order, OrderItem, OrderStatus, Product, ProductVariant, UserAddress, VariantConfig, VariantOption



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

            for i in item_mappings:
                i["order_id"] = order.id

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
            error(f"Error creating order: {e}")
            return None
        

    async def set_order_status(self, order_id: str, user_id: str, status: OrderStatus):
        stmt = update(Order).where(
            and_(
                Order.id == order_id,
                Order.user_id == user_id
            )
        )
        stmt = stmt.values(
            {"status":status}
        ).returning(
            Order.id,
            Order.status,
            Order.total_amount,
            Order.discount_amount,
            Order.final_amount,
            Order.created_at
        )

        try:
            result = await self.session.execute(stmt)
            return result
        except Exception as e:
            error(f"set order-status error: {e}")
            return None

    async def get_user_orders(
            self, 
            user_id: str,
            status: Optional[OrderStatus] = None # none = all
        ) -> List[Order]:
        stmt = (
            select(Order)
            .options(
                load_only(
                    Order.id,
                    Order.total_amount,
                    Order.discount_amount,
                    Order.final_amount,
                    Order.status,
                    Order.created_at
                )
            )
            .where(Order.user_id == user_id)
        )

        if status is not None:
            stmt = stmt.where(
                Order.status == status
            )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_order_by_id(self, order_id: str, user_id: str) -> Optional[Order]:    
        stmt = (
            select(Order)
            .where(
                Order.id == order_id,
                Order.user_id == user_id
            )
            .options(
                load_only(
                    Order.id,
                    Order.total_amount,
                    Order.discount_amount,
                    Order.final_amount,
                    Order.status,
                    Order.description,
                    Order.transaction_id,
                    Order.paid_at,
                    Order.created_at
                ),
                selectinload(Order.address).load_only(
                    UserAddress.id,
                    UserAddress.phone_number,
                    UserAddress.postal_code,
                    UserAddress.address_line,
                ),
                selectinload(Order.items).options(
                    load_only(
                        OrderItem.quantity,
                        OrderItem.unit_price,
                        OrderItem.variant_price_override,
                        OrderItem.discounted_price,
                        OrderItem.total_price,
                    ),
                    selectinload(OrderItem.product).load_only(
                        Product.id,
                        Product.name,
                        Product.base_price,
                        Product.main_image,
                        Product.created_at,
                    ),
                    selectinload(OrderItem.variant).load_only(
                        ProductVariant.id,
                        ProductVariant.price_override,
                        ProductVariant.is_active,
                        ProductVariant.stock
                    )
                    .selectinload(ProductVariant.config).load_only(
                        VariantConfig.option_id,
                        VariantConfig.value,
                    )
                    .selectinload(VariantConfig.option).load_only(
                        VariantOption.name, VariantOption.label
                    )
                )
            )
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
    