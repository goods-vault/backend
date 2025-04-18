from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class NetContent(BaseModel):
    unit: str
    value: int


class Product(BaseModel):
    gtin: str
    brand: str
    title: str
    image: str | None
    net_content: NetContent
    category: str
    updated_at: datetime


class AppStatus(BaseModel):
    status: Literal["healthy"]
    timestamp: datetime


class HTTPError(BaseModel):
    detail: str
