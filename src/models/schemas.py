from datetime import datetime
from typing import Literal

from pydantic import BaseModel, HttpUrl, Field, ConfigDict


class NetContent(BaseModel):
    unit: str | None
    value: float | None

    model_config = ConfigDict(from_attributes=True)


class Product(BaseModel):
    gtin: str
    brand: str | None
    title: str
    image: HttpUrl | None
    net_content: NetContent
    category_id: int
    category: str = Field(..., alias="category_title")
    updated_at: datetime = Field(..., alias="updated_in_gs1_at")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class AppStatus(BaseModel):
    status: Literal["healthy"]
    timestamp: datetime


class HTTPError(BaseModel):
    detail: str
