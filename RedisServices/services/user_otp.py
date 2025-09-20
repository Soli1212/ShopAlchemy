from aioredis import Redis
from logging import error
from typing import Optional, Dict


class UserOtpService:
    def __init__(self, redis_client: Redis):
        """Initialize UserOtpService with Redis client."""
        self.redis = redis_client
    
    async def save_otp(self, phone: str, otp: int, expiry: int = 180) -> bool:
        """Save OTP for phone number with expiry time."""
        try:
            await self.redis.set(phone, otp, ex=expiry)
            return True
        except Exception as e:
            error(f"Error saving OTP for user {phone}: {e}")
            return False
    
    async def get_otp(self, phone: str) -> Optional[int]:
        """Retrieve OTP for phone number."""
        try:
            otp = await self.redis.get(phone)
            return int(otp) if otp else None
        except Exception as e:
            error(f"Error retrieving OTP for user {phone}: {e}")
            return None
        
    async def delete_otp(self, phone: str) -> bool:
        """Delete OTP for phone number."""
        try:
            await self.redis.delete(phone)
            return True
        except Exception as e:
            error(f"Error deleting OTP for user {phone}: {e}")
            return False
        
    async def otp_exists(self, phone: str) -> bool:
        """Check if OTP exists for phone number."""
        try:
            exists = await self.redis.exists(phone)
            return exists == 1
        except Exception as e:
            error(f"Error checking OTP existence for user {phone}: {e}")
            return False