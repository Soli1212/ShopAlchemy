from datetime import datetime
from logging import error
from typing import Optional

from sqlalchemy import and_, func, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import UserAddress


class UserAddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def unset_all_defaults(self, user_id: str) -> bool:
        """Set all addresses of a user to is_default = False"""
        stmt = (
            update(UserAddress)
            .where(UserAddress.user_id == user_id)
            .values(is_default=False)
        )
        try:
            await self.session.execute(stmt)
            return True
        except Exception as e:
            error(f"Error creating user address: {e}")
            return False

    async def create(
        self,
        user_id: str,
        full_name: str,
        phone_number: str,
        province: str,
        city: str,
        postal_code: str,
        plaque: str,
        address_line: str,
        is_default: bool,
    ) -> Optional[UserAddress]:
        """Add new address for a user"""
        stmt = (
            insert(UserAddress)
            .values(
                user_id=user_id,
                full_name=full_name,
                phone_number=phone_number,
                province=province,
                city=city,
                postal_code=postal_code,
                plaque=plaque,
                address_line=address_line,
                is_default=is_default,
                created_at=datetime.utcnow(),
            )
            .returning(UserAddress)
        )
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except Exception as e:
            error(f"Error creating user address: {e}")
            return None

    async def update_address(
        self,
        address_id: int,
        user_id: str,
        full_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        province: Optional[str] = None,
        city: Optional[str] = None,
        postal_code: Optional[str] = None,
        plaque: Optional[str] = None,
        address_line: Optional[str] = None,
        is_default: Optional[bool] = None,
    ) -> Optional[UserAddress]:
        """Update user address safely by explicit params only"""

        update_data = {
            "full_name": full_name,
            "phone_number": phone_number,
            "province": province,
            "city" : city,
            "postal_code" : postal_code,
            "plaque" : plaque,
            "address_line" : address_line,
            "is_default" : is_default
        }

        update_data = {k : v for k, v in update_data.items() if v is not None}

        if not update_data:
            return None

        stmt = (
            update(UserAddress)
            .where(UserAddress.id == address_id, UserAddress.user_id == user_id)
            .values(**update_data)
            .returning(UserAddress)
        )

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()

        except Exception as e:
            error(f"Error updating address: {e}")
            return None

    async def delete_address(self, address_id: int, user_id: str) -> bool:
        """delete user address"""
        stmt = select(UserAddress).where(
            UserAddress.id == address_id, UserAddress.user_id == user_id
        )
        result = await self.session.execute(stmt)
        address = result.scalar_one_or_none()
        if address:
            await self.session.delete(address)
            return True
        return False

    async def get_user_addresses(self, user_id: str) -> list[UserAddress]:
        """Get a list of user addresses"""
        stmt = select(UserAddress).where(UserAddress.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_default_address(self, user_id: str) -> Optional[UserAddress]:
        """Get the user's default address"""
        stmt = select(UserAddress).where(
            and_(
                UserAddress.user_id == user_id,
                UserAddress.is_default == True,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def count_user_addresses(self, user_id: int) -> int:
        """Get the total number of user addresses"""
        stmt = (
            select(func.count())
            .select_from(UserAddress)
            .where(UserAddress.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()
