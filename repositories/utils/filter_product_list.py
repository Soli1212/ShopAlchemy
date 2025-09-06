from typing import Optional

from sqlalchemy import Select, and_, case, literal, select

from models import Product, ProductVariant

availability_subquery = (
    select(ProductVariant.id)
    .where(
        and_(
            ProductVariant.product_id == Product.id,
            ProductVariant.is_active == True,
            ProductVariant.stock > 0,
        )
    )
    .exists()
)


def apply_filters(
    query: Select,
    brand_id: Optional[int] = None,
    existing: bool = True,
    price_zone: Optional[tuple[int, int]] = None,
) -> Select:

    if not existing:
        query = query.add_columns(
            case((availability_subquery, True), else_=False).label("is_available")
        )
    else:
        query = query.add_columns(literal(True).label("is_available"))
        query = query.where(availability_subquery)

    if brand_id:
        query = query.where(Product.brand_id == brand_id)

    if price_zone:
        query = query.where(Product.base_price.between(price_zone[0], price_zone[1]))

    return query
