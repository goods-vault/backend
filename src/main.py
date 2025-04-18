from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

import uvicorn
from db import create_tables
from exceptions import ProductNotExists
from fastapi import FastAPI, HTTPException
from models.schemas import Product, AppStatus, HTTPError
from pydantic import AfterValidator
from services.gs1ru_client import GS1RUClient
from settings import settings
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


@app.get("/api/product", responses={404: {"model": HTTPError}})
async def get_product(code: Annotated[str, AfterValidator(check_valid_code)]) -> Product:
    client = GS1RUClient()

    try:
        product = await client.get_product(code)
        return Product(**product)

    except ProductNotExists:
        raise HTTPException(
            status_code=404,
            detail="This product does not exist in the GS1 database"
        )


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.api_host,
                port=settings.api_port,
                reload=settings.debug)
