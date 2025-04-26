from datetime import datetime
from typing import Literal

from pydantic import BaseModel, HttpUrl


class NetContent(BaseModel):
    unit: str | None
    value: float | None


class Product(BaseModel):
    gtin: str
    brand: str | None
    title: str
    image: HttpUrl | None
    net_content: NetContent
    category: str
    updated_at: datetime


class AppStatus(BaseModel):
    status: Literal["healthy"]
    timestamp: datetime


class HTTPError(BaseModel):
    detail: str
