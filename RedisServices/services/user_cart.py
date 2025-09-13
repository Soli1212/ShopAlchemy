from aioredis import Redis
from logging import error
from typing import Optional, Dict


class UserCartService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def add_item(
        self, user_id: str, product_variant_id: str, quantity: int
    ) -> bool:
        try:
            await self.redis.hset(f"cart:{user_id}", product_variant_id, quantity)
            return True
        except Exception as e:
            error(e)
            return False

    async def remove_item(self, user_id: str, product_variant_id: str) -> bool:
        try:
            await self.redis.hdel(f"cart:{user_id}", product_variant_id)
            return True
        except Exception as e:
            error(e)
            return False

    async def edit_item(
        self, user_id: str, product_variant_id: str, quantity: int
    ) -> bool:
        try:
            await self.redis.hset(f"cart:{user_id}", product_variant_id, quantity)
            return True
        except Exception as e:
            error(e)
            return False

    async def get_cart(self, user_id: str) -> Optional[Dict]:
        try:
            cart = await self.redis.hgetall(f"cart:{user_id}")
            return {key: int(value) for key, value in cart.items()}
        except Exception as e:
            error(e)
            return None
