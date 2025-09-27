from logging import error

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only, selectinload
from .utils import apply_sorting_and_keyset, Sorting
from typing import Optional
from enum import Enum

from models import (
    Attribute,
    Brand,
    Category,
    Product,
    ProductAttribute,
    ProductCategory,
    ProductTag,
    ProductVariant,
    Tag,
    VariantConfig,
    VariantImage,
    VariantOption,
)

class target_product(Enum):
    discouunted = "discounted",
    suggested = "suggested",
    trend = "trend",


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_product_by_id(self, product_id: str):
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                load_only(
                    Product.id,
                    Product.name,
                    Product.description,
                    Product.base_price,
                    Product.discount_percentage,
                    Product.main_image,
                    Product.lux,
                    Product.suggested,
                    Product.trend,
                    Product.created_at,
                ),
                joinedload(Product.product_categories)
                .load_only()
                .joinedload(ProductCategory.category)
                .load_only(Category.id, Category.name, Category.image_url),
                joinedload(Product.product_tags)
                .load_only()
                .joinedload(ProductTag.tag)
                .load_only(Tag.id, Tag.name),
                joinedload(Product.brand).load_only(
                    Brand.id, Brand.name, Brand.image_url
                ),
                selectinload(Product.product_attributes)
                .load_only(ProductAttribute.value)
                .joinedload(ProductAttribute.attribute)
                .load_only(Attribute.id, Attribute.name, Attribute.label),
                selectinload(Product.variants)
                .load_only(
                    ProductVariant.id,
                    ProductVariant.sku,
                    ProductVariant.price_override,
                    ProductVariant.stock,
                    ProductVariant.is_active,
                )
                .joinedload(ProductVariant.config)
                .load_only(VariantConfig.id, VariantConfig.value)
                .joinedload(VariantConfig.option)
                .load_only(VariantOption.id, VariantOption.name, VariantOption.label),
                selectinload(Product.variants)
                .selectinload(ProductVariant.images)
                .load_only(
                    VariantImage.id, VariantImage.image_url, VariantImage.alt_text
                ),
            )
        )

        try:
            result = await self.session.execute(stmt)
            product = result.unique().scalars().first()

            return product
        except Exception as e:
            error(f"Error fetching product by id {product_id}: {e}")
            return None
        
    async def get_special_products(
            self,
            last_id: Optional[str] = None,
            last_sort_value: Optional[str] = None,
            target_products: Enum = None,
            page_size: int = 15,
        ):
        stmt = select(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            Product.base_price.label("product_price"),
            Product.discount_percentage,
            Product.main_image,
            Product.created_at,
        )
        match target_products:
            case target_product.discouunted:
                stmt = stmt.where(Product.discount_percentage > 0)
                sort_as = Sorting.discount
            case target_product.suggested:
                stmt = stmt.where(Product.suggested == True)
                sort_as = Sorting.new_desc
            case target_product.trend:
                stmt = stmt.where(Product.trend == True)
                sort_as = Sorting.new_desc
        try:
            stmt = apply_sorting_and_keyset(
                query=stmt,
                sort_as=sort_as,
                last_id=last_id,
                last_value=last_sort_value,
                page_size=page_size + 1,
            )

            result = await self.session.execute(stmt)
            rows = result.mappings().all()

            items = rows[:page_size]
            has_next = len(rows) > page_size

            return {
                "items": items,
                "next_page": has_next,
            }

        except Exception as e:
            error(f"Error fetching discounted products: {e}")
            return None
        