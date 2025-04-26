from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import AfterValidator
from sqlalchemy.ext.asyncio import AsyncSession

from db import create_tables, get_db
from exceptions import ProductNotExists
from models.schemas import Product as ProductSchema, AppStatus, HTTPError
from models.utils.product import get_product_by_gtin, create_product, get_unique_brands
from services.gs1ru_client import GS1RUClient
from settings import settings
from utils import ean2gtin
from validators import check_valid_code


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/health")
async def get_health() -> AppStatus:
    return AppStatus(**{
        "status": "healthy",
        "timestamp": datetime.now(),
    })


@app.get(
    "/api/product",
    response_model=ProductSchema,
    response_model_by_alias=False,
    responses={404: {"model": HTTPError}},
)
async def get_product(
        code: Annotated[str, AfterValidator(check_valid_code)],
        db: AsyncSession = Depends(get_db),
) -> ProductSchema:
    gtin = ean2gtin(code)
    product = await get_product_by_gtin(db, gtin)
    if product:
        return ProductSchema.model_validate(product)

    client = GS1RUClient(db)
    try:
        product = await client.get_product(code)
        product = ProductSchema(**product)
        await create_product(db, product)
        return product

    except ProductNotExists:
        raise HTTPException(
            status_code=404,
            detail="This product does not exist in the GS1 database",
        )


@app.get("/api/brands")
async def get_brands(db: AsyncSession = Depends(get_db)) -> list[str]:
    return await get_unique_brands(db)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.api_host,
                port=settings.api_port,
                reload=settings.debug)
