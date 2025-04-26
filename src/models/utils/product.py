from typing import cast

from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm import Product as ProductORM
from models.schemas import Product as ProductSchema


async def create_product(db: AsyncSession, product: ProductSchema) -> ProductORM:
    product = ProductORM(
        gtin=product.gtin,
        brand=product.brand,
        title=product.title,
        image=str(product.image) if product.image else None,
        net_content_unit=product.net_content.unit,
        net_content_value=product.net_content.value,
        category_id=product.category_id,
        updated_in_gs1_at=product.updated_at,
    )
    db.add(product)

    await db.commit()
    await db.refresh(product)
    return product


async def get_product_by_gtin(db: AsyncSession, gtin: str) -> ProductORM | None:
    result = await db.execute(select(ProductORM).filter(ProductORM.gtin == gtin))
    return result.scalars().first()

async def get_unique_brands(db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(distinct(ProductORM.brand))
        .where(ProductORM.brand != None)
        .order_by(ProductORM.brand)
    )
    return cast(list[str], result.scalars().all())
