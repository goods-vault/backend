from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

import uvicorn
from db import create_tables
from fastapi import FastAPI
from pydantic import AfterValidator
from settings import settings
from validators import check_valid_code


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/health")
async def get_health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/product")
async def get_product(code: Annotated[str, AfterValidator(check_valid_code)]):
    ...


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.api_host,
                port=settings.api_port,
                reload=settings.debug)
