from datetime import datetime
from enum import Enum
from typing import Optional

from dateutil.parser import isoparse
from sqlalchemy import UUID, Select, cast

from models import Product


class Sorting(Enum):
    price_asc = "price_asc"
    price_desc = "price_desc"
    new_desc = "new_desc"
    discount = "discount"
    id_asc = "id_asc"


def parse_iso_datetime(s: str) -> datetime:
    s = s.replace(" ", "+")
    if "+" not in s and "Z" not in s:
        s += "+00:00"
    try:
        return datetime.fromisoformat(s)
    except:
        return None


def apply_sorting_and_keyset(
    query: Select,
    sort_as: Sorting = Sorting.id_asc,
    last_id: Optional[str] = None,
    last_value: Optional[str] = None,
    page_size: int = 15,
) -> Select:

    match sort_as:
        case Sorting.price_asc:
            if last_value is not None and last_id:
                query = query.where(
                    (Product.base_price > float(last_value))
                    | (
                        (Product.base_price == float(last_value))
                        & (cast(Product.id, UUID) > cast(last_id, UUID))
                    )
                )
            order = [Product.base_price.asc(), cast(Product.id, UUID).asc()]

        case Sorting.price_desc:
            if last_value is not None and last_id:
                query = query.where(
                    (Product.base_price < float(last_value))
                    | (
                        (Product.base_price == float(last_value))
                        & (cast(Product.id, UUID) > cast(last_id, UUID))
                    )
                )
            order = [Product.base_price.desc(), cast(Product.id, UUID).asc()]

        case Sorting.new_desc:
            if last_value is not None and last_id:
                created_at_val = parse_iso_datetime(last_value)
                if created_at_val:
                    query = query.where(
                        (Product.created_at < created_at_val)
                        | (
                            (Product.created_at == created_at_val)
                            & (cast(Product.id, UUID) > cast(last_id, UUID))
                        )
                    )
            order = [Product.created_at.desc(), cast(Product.id, UUID).asc()]

        case Sorting.discount:
            if last_value is not None and last_id:
                query = query.where(
                    (Product.discount_percentage < int(last_value))
                    | (
                        (Product.discount_percentage == int(last_value))
                        & (cast(Product.id, UUID) > cast(last_id, UUID))
                    )
                )
            order = [Product.discount_percentage.desc(), cast(Product.id, UUID).asc()]

        case Sorting.id_asc:
            if last_id:
                query = query.where(cast(Product.id, UUID) > cast(last_id, UUID))
            order = [cast(Product.id, UUID).asc()]

    return query.order_by(*order).limit(page_size)
