from datetime import datetime
from typing import Optional

from sqlalchemy import and_, desc, exists, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Order, User, UserAddress
from models.user import Gender


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, phone_number: str, first_name: str = None, last_name: str = None
    ) -> Optional[str]:
        """Add new user"""
        stmt = (
            insert(User)
            .values(
                first_name=first_name, last_name=last_name, phone_number=phone_number
            )
            .returning(User.id)
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalars().first()
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    async def exists_by_phone_number(self, phone_number: str) -> bool:
        """Checking the existence of a phone number"""
        stmt = select(exists().where(User.phone_number == phone_number))
        result = await self.session.execute(stmt)
        return bool(result.scalar())

    async def get_profile(self, user_id: str):
        """get user profile"""
        subquery = (
            select(
                Order.id.label("order_id"),
                Order.status,
                Order.final_amount,
                Order.user_id,
            )
            .where(Order.user_id == user_id)
            .order_by(desc(Order.created_at))
            .limit(3)
            .subquery()
        )
        stmt = (
            select(
                User.id,
                User.first_name,
                User.last_name,
                User.phone_number,
                User.email,
                User.birth_date,
                User.gender,
                UserAddress.id.label("address_id"),
                UserAddress.full_name,
                UserAddress.phone_number,
                UserAddress.address_line,
                subquery.c.order_id,
                subquery.c.status,
                subquery.c.final_amount,
            )
            .outerjoin(
                UserAddress,
                and_(UserAddress.user_id == User.id, UserAddress.is_default == True),
            )
            .outerjoin(subquery, subquery.c.user_id == User.id)
            .where(User.id == user_id)
        )

        try:
            result = await self.session.execute(stmt)
            return result.fetchone()
        except Exception as e:
            print(f"Error fetching user profile: {e}")
            return None

    async def update_user_info(
        self,
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        birth_date: Optional[datetime] = None,
        gender: Optional[Gender] = None,
    ) -> Optional[User]:
        """update user profile"""
        update_data = {}
        if first_name is not None:
            update_data["first_name"] = first_name
        if last_name is not None:
            update_data["last_name"] = last_name
        if email is not None:
            update_data["email"] = email
        if birth_date is not None:
            update_data["birth_date"] = birth_date
        if gender is not None:
            update_data["gender"] = gender

        if not update_data:
            return False

        stmt = (
            update(User).where(User.id == user_id).values(**update_data).returning(User)
        )
        try:
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            print(f"Error updating user info: {e}")
            return False
