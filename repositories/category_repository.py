from logging import error
from typing import Any, Dict, List, Optional

from sqlalchemy import UUID, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only

from models import Category, Product, ProductCategory

from .utils import Sorting, apply_filters, apply_sorting_and_keyset


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Cache result on redis for performance
    async def category_tree(self) -> List[Category]:
        stmt = (
            select(Category)
            .options(
                load_only(Category.id, Category.name, Category.image_url),
                joinedload(Category.children).options(
                    load_only(Category.id, Category.name, Category.image_url),
                    joinedload(Category.children).options(
                        load_only(Category.id, Category.name, Category.image_url),
                        joinedload(Category.children).options(
                            load_only(Category.id, Category.name, Category.image_url)
                        ),
                    ),
                ),
            )
            .filter(Category.parent_id == None)
        )
        try:
            result = await self.session.execute(stmt)
            return result.unique().scalars().all()
        except Exception as e:
            error(f"Error get category_tree: {e}")
            return None


    async def get_categories_products(
        self,
        category_ids: List[int],
        brand_id: Optional[int] = None,
        page_size: int = 15,
        existing: bool = True,
        price_zone: Optional[tuple[int, int]] = None,
        sort_as: Sorting = Sorting.id_asc,
        last_id: Optional[str] = None,
        last_sort_value: Optional[str] = None,
    ) -> Dict[str, Any]:
        stmt = (
            select(
                Product.id.label("product_id"),
                Product.name.label("product_name"),
                Product.base_price.label("product_price"),
                Product.discount_percentage,
                Product.main_image,
                Product.created_at,
            )
            .join(ProductCategory, Product.id == ProductCategory.product_id)
            .filter(ProductCategory.category_id.in_(category_ids))
        )

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

        try:
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
