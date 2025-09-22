from asyncio import run
from pprint import pprint

from RedisServices.connection import RedisConnection
from RedisServices.services import UserCartService

from repositories import CartRepository
from connection import get_db 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends

app = FastAPI()



@app.get('/')
async def main(db: AsyncSession = Depends(get_db)):
    connection = await RedisConnection.connect()
    c = UserCartService(redis_client=connection)
    r = await c.get_cart("soheil")
    product_list = [i for i in r]
    products = CartRepository(session=db)
    cart = await products.get_cart(product_list)
    return cart



