from logging import error

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, load_only, selectinload

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
                    Product.new,
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
