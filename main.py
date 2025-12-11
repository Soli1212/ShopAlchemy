from fastapi import FastAPI, Depends, Query, HTTPException
from repositories import ProductRepository
from repositories.brand_repository import BrandRepository
from connection import get_db

from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()

@app.get("/random")
async def get_random_products(
    db: AsyncSession = Depends(get_db),
    text: str = Query()
):
    b = BrandRepository(session=db)

    return await b.search_brands(
        query = text
    )