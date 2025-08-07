from datetime import datetime
from typing import Optional

from sqlalchemy import and_, insert, update
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
            print(f"Error creating user address: {e}")
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
            print(f"Error creating user address: {e}")
            return None

    async def update_address(
        self,
        address_id: int,
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

        update_data = {}

        if full_name is not None:
            update_data["full_name"] = full_name
        if phone_number is not None:
            update_data["phone_number"] = phone_number
        if province is not None:
            update_data["province"] = province
        if city is not None:
            update_data["city"] = city
        if postal_code is not None:
            update_data["postal_code"] = postal_code
        if plaque is not None:
            update_data["plaque"] = plaque
        if address_line is not None:
            update_data["address_line"] = address_line
        if is_default is not None:
            update_data["is_default"] = is_default

        if not update_data:
            return None

        stmt = (
            update(UserAddress)
            .where(UserAddress.id == address_id)
            .values(**update_data)
            .returning(UserAddress)
        )

        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()

        except Exception as e:
            print(f"Error updating address: {e}")
            return None

    async def delete_address(self, address_id: int) -> bool:
        stmt = select(UserAddress).where(UserAddress.id == address_id)
        result = await self.session.execute(stmt)
        address = result.scalar_one_or_none()
        if address:
            await self.session.delete(address)
            await self.session.commit()
            return True
        return False

    async def get_user_addresses(self, user_id: str) -> list[UserAddress]:
        stmt = select(UserAddress).where(UserAddress.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_default_address(self, user_id: str) -> Optional[UserAddress]:
        stmt = select(UserAddress).where(
            and_(
                UserAddress.user_id == user_id,
                UserAddress.is_default == True,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
