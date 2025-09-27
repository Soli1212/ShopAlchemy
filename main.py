from asyncio import run
from pprint import pprint

from RedisServices.connection import RedisConnection
from RedisServices.services import UserCartService

from repositories import OrderRepository, CartRepository, ProductRepository
from repositories.product_repository import target_product
from connection import get_db 
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, Depends

from models import OrderItem
from typing import Optional

from enum import Enum

app = FastAPI()



@app.get('/')
async def index():
    return "HI 😃"

