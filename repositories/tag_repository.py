from logging import error

from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import cast, UUID
from sqlalchemy.orm import joinedload, load_only, selectinload
from .utils import Sorting, apply_filters, apply_sorting_and_keyset

from models import Tag, ProductTag, Product


class TagRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tag_list(  
        self,
        last_id: int = 0,
        page_size: int = 10,
    ) -> Dict:
        stmt = select(Tag.id, Tag.name).where(Tag.id > last_id)

        stmt = stmt.order_by(Tag.id).limit(page_size + 1)

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

    async def get_tag_products(
        self,
        tag_id: int,
        brand_id: Optional[int] = None,
        page_size: int = 15,
        existing: bool = True,
        price_zone: Optional[tuple[int, int]] = None,
        sort_as: Sorting = Sorting.id_asc,
        last_id: Optional[str] = None,
        last_sort_value: Optional[str] = None,
    ) -> Dict:
        stmt = (
            select(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.base_price.label("product_price"),
                Product.discount_percentage,
                Product.main_image,
                Product.created_at,
            )
            .join(ProductTag, Product.id == ProductTag.product_id)
            .filter(ProductTag.tag_id == tag_id)
        )
        try:
            stmt = apply_filters(
                query=stmt,
                brand_id=brand_id,
                existing=existing,
                price_zone=price_zone,
            )

            stmt = apply_sorting_and_keyset(
                query=stmt,
                sort_as=sort_as,
                last_id=last_id,
                last_value=last_sort_value,
                page_size=page_size + 1,
            )

            match sort_as:
                case Sorting.price_asc | Sorting.price_desc:
                    stmt = stmt.distinct(Product.base_price, cast(Product.id, UUID))
                case Sorting.new_desc:
                    stmt = stmt.distinct(Product.created_at, cast(Product.id, UUID))
                case Sorting.discount:
                    stmt = stmt.distinct(
                        Product.discount_percentage, cast(Product.id, UUID)
                    )
                case Sorting.id_asc:
                    stmt = stmt.distinct(cast(Product.id, UUID))

            result = await self.session.execute(stmt)
            rows = result.mappings().all()

            items = rows[:page_size]
            has_next = len(rows) > page_size

            return {
                "items": items,
                "next_page": has_next,
            }
        except Exception as e:
            error(f"Error searching category products: {e}")
            return None
