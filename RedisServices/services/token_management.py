from aioredis import Redis

class TokenManagementService:
    def __init__(self, redis_client: Redis):
        """Initialize TokenManagementService with Redis client."""
        self.redis = redis_client

    async def block_token(self, token: str, expiry: int):
        key = f"blocked_token:{token}"
        await self.redis.set(key, "blocked", ex=expiry)

    async def is_token_blocked(self, token: str) -> bool:
        key = f"blocked_token:{token}"
        result = await self.redis.exists(key)
        return result == 1