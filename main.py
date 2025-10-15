from asyncio import run
from enum import Enum
from pprint import pprint
from typing import Optional

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from connection import get_db
from models import OrderItem
from RedisServices.connection import RedisConnection
from RedisServices.services import UserCartService
from repositories import CartRepository, OrderRepository, ProductRepository
from repositories.product_repository import target_product
from repositories.order_repository import OrderStatus

app = FastAPI()


@app.get("/")
async def index(db: AsyncSession = Depends(get_db)):
    repo = OrderRepository(session=db)

    return await repo.get_order_by_id(
        user_id= "018c7e5b-4b1a-7c3e-9f2a-1b3c4d5e6f7d",
        order_id="01997ded-b818-79f8-b248-98a1ca793442"
    )
