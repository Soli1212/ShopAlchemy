from aioredis import Redis, from_url
from os import getenv
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

load_dotenv()
redis_url: str = getenv("REDIS_URL", "redis://localhost:6379/0")


class RedisConnection:
    client: Redis = None

    @classmethod
    async def connect(cls) -> Redis:
        if cls.client:
            return cls.client
        try:
            logger.info("Connecting to Redis...")
            cls.client = from_url(redis_url, decode_responses=True)
            await cls.get_ping()
            logger.info("Connected to Redis")
            return cls.client
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise e

    @classmethod
    async def get_ping(cls) -> str:
        if cls.client is None:
            raise Exception("Redis client is not connected.")
        return await cls.client.ping()

    @classmethod
    async def disconnect(cls):
        if cls.client:
            try:
                await cls.client.close()
                logger.info("Disconnected from Redis")
            except Exception as e:
                logger.error(f"Error disconnecting from Redis: {e}")

    @classmethod
    async def reconnect(cls):
        try:
            if cls.client is None:
                await cls.connect()
            else:
                logger.info("Already connected to Redis.")
        except Exception as e:
            logger.error(f"Failed to reconnect to Redis: {e}")
