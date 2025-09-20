from aioredis import Redis
from logging import error
from typing import Optional, Dict


class UserCartService:
    def __init__(self, redis_client: Redis):
        """Initialize UserCartService with Redis client."""
        self.redis = redis_client

    async def add_item(
        self, user_id: str, product_variant_id: str, quantity: int
    ) -> bool:
        """Add item to user's cart with quantity."""
        try:
            await self.redis.hset(f"cart:{user_id}", product_variant_id, quantity)
            self.redis.expire(f"cart:{user_id}", 172800)  # 2 days in seconds
            return True
        except Exception as e:
            error(e)
            return False

    async def remove_item(self, user_id: str, product_variant_id: str) -> bool:
        """Remove item from user's cart."""
        try:
            await self.redis.hdel(f"cart:{user_id}", product_variant_id)
            return True
        except Exception as e:
            error(e)
            return False

    async def edit_item(
        self, user_id: str, product_variant_id: str, quantity: int
    ) -> bool:
        """Edit item quantity in user's cart."""
        try:
            await self.redis.hset(f"cart:{user_id}", product_variant_id, quantity)
            return True
        except Exception as e:
            error(e)
            return False

    async def get_cart(self, user_id: str) -> Optional[Dict]:
        """Retrieve user's cart from Redis."""
        try:
            cart = await self.redis.hgetall(f"cart:{user_id}")
            return {key: int(value) for key, value in cart.items()}
        except Exception as e:
            error(e)
            return None