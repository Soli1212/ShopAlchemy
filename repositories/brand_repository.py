from logging import error
from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Brand, Product

from .utils import Sorting, apply_filters, apply_sorting_and_keyset


class BrandRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def brand_list(
        self,
        last_id: int = 0,
        page_size: int = 10,
    ) -> Dict:
        stmt = select(Brand.id, Brand.name, Brand.image_url).where(Brand.id > last_id)

        stmt = stmt.order_by(Brand.id).limit(page_size + 1)

        try:
            result = await self.session.execute(stmt)
            rows = result.mappings().fetchall()

            items = rows[:page_size]
            has_next = len(rows) > page_size

            return {
                "items": items,
                "next_page": has_next,
            }

        except Exception as e:
            error(f"Error fetching brand list: {e}")
            return None

    async def search_brands(self, query: str, limit: int = 15) -> list[dict]:
        stmt = (
            select(Brand.id, Brand.name, Brand.image_url)
            .where(Brand.name.ilike(f"%{query}%"))
            .limit(limit)
        )
        try:
            result = await self.session.execute(stmt)
            return result.mappings().all()
        except Exception as e:
            error(f"Error searching brands: {e}")
            return None

    async def brand_products(
        self,
        brand_id: int,
        page_size: int = 15,
        existing: bool = True,
        price_zone: Optional[tuple[int, int]] = None,
        sort_as: Sorting = Sorting.id_asc,
        last_id: Optional[str] = None,
        last_sort_value: Optional[str] = None,
    ) -> Dict:

        stmt = select(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Product.base_price.label("product_price"),
            Product.discount_percentage,
            Product.main_image,
            Product.created_at,
        )
        stmt = stmt.where(Product.brand_id == brand_id)

        try:
            stmt = apply_filters(
                query=stmt, brand_id=brand_id, existing=existing, price_zone=price_zone
            )

            stmt = apply_sorting_and_keyset(
                query=stmt,
                sort_as=sort_as,
                last_id=last_id,
                last_value=last_sort_value,
                page_size=page_size + 1,
            )

            stmt.distinct(Product.id)

            result = await self.session.execute(stmt)
            rows = result.mappings().all()

            items = rows[:page_size]
            has_next = len(rows) > page_size

            return {
                "items": items,
                "next_page": has_next,
            }

        except Exception as e:
            error(f"Error searching brand products: {e}")
            return None

    async def serach_brand(self, brand_name: str) -> Optional[Dict]:
        stmt = select(Brand).where(Brand.name.ilike(f"%{brand_name}%"))

        try:
            result = await self.session.execute(stmt)
            return result.scalars().fetchmany()
        except:
            error(f"Error searching brand by name {brand_name}")
            return None