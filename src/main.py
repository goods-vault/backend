from datetime import datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import AfterValidator
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from exceptions import ProductNotExists, InvalidCaptchaToken
from logging_config import configure_logging
from models.schemas import Product as ProductSchema, AppStatus, HTTPError, Category
from models.utils.product import (get_product_by_gtin, create_product, get_used_unique_brands,
                                  get_used_categories, get_used_categories_from_root, build_used_categories_tree)
from services.gs1ru_client import GS1RUClient
from settings import settings
from utils import ean2gtin
from validators import check_valid_code

configure_logging()
app = FastAPI()


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
    responses={
        403: {"model": HTTPError},
        404: {"model": HTTPError},
    },
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
            detail="This product does not exist in the GS1 database.",
        )

    except InvalidCaptchaToken:
        raise HTTPException(
            status_code=403,
            detail="Invalid or expired captcha token. "
                   "It must be replaced on the backend. "
                   "Notice that the token is valid for 24 hours.",
        )


@app.get("/api/brands")
async def get_brands(db: AsyncSession = Depends(get_db)) -> set[str | None]:
    return await get_used_unique_brands(db)


@app.get("/api/categories", response_model=list[Category])
async def get_categories(db: AsyncSession = Depends(get_db)):
    used_categories = await get_used_categories(db)
    used_categories = get_used_categories_from_root(used_categories)
    return build_used_categories_tree(used_categories)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.api_host,
                port=settings.api_port,
                reload=settings.debug)
