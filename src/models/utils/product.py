from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm import Product as ProductORM
from models.schemas import Product as ProductSchema


async def create_product(db: AsyncSession, product: ProductSchema) -> ProductORM:
    product = ProductORM(
        gtin=product.gtin,
        brand=product.brand,
        title=product.title,
        image=product.image,
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
