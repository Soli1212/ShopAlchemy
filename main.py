from asyncio import run
from pprint import pprint

from RedisServices.connection import RedisConnection
from RedisServices.services import UserCartService

from repositories import OrderRepository, CartRepository, ProductRepository
from connection import get_db 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends

from models import OrderItem

app = FastAPI()



@app.get('/')
async def main(db: AsyncSession = Depends(get_db)):
    repo = CartRepository(session=db)
    cart = await repo.get_cart(
        variant_ids=[
            "018c7e5b-4b1a-7c3e-9f2a-1b3c4d5e6fb6",
            "018c7e5b-4b1a-7c3e-9f2a-1b3c4d5e6fb8",
            "018c7e5b-4b1a-7c3e-9f2a-1b3c4d5e6fb7"
        ]
    )
    return cart

@app.get('/{p_id}')
async def main(p_id: str, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(session=db)
    return await repo.get_product_by_id(product_id=p_id)

