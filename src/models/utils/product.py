from typing import cast

from sqlalchemy import select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.orm import Product as ProductORM, Category as CategoryORM
from models.schemas import Product as ProductSchema, Category as CategorySchema


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


async def get_used_unique_brands(db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(distinct(ProductORM.brand))
        .where(ProductORM.brand != None)
        .order_by(ProductORM.brand)
    )
    return cast(list[str], result.scalars().all())


async def get_used_categories(db: AsyncSession) -> list[CategoryORM]:
    result = await db.execute(
        select(CategoryORM)
        .join(ProductORM, CategoryORM.id == ProductORM.category_id)
        .options(
            selectinload(CategoryORM.parent)
            .selectinload(CategoryORM.parent)
            .selectinload(CategoryORM.parent),
        )
        .distinct()
    )
    return result.scalars().all()


def get_used_categories_from_root(used_categories: list[CategoryORM]) -> set[CategoryORM]:
    categories = set()

    for category in used_categories:
        categories.update([category.parent, category.parent.parent, category.parent.parent.parent])

    return categories


def build_used_categories_tree(used_categories: set[CategoryORM]) -> list[CategorySchema]:
    id_to_node: dict[int, CategorySchema] = {}
    for category in used_categories:
        id_to_node[category.id] = CategorySchema(
            id=category.id,
            title=category.title,
        )

    roots: list[CategorySchema] = []
    for category in used_categories:
        node = id_to_node[category.id]

        if not category.parent_id or category.parent_id not in id_to_node:
            roots.append(node)
        else:
            parent = id_to_node[category.parent_id]
            parent.children.append(node)

    return roots
