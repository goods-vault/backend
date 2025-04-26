from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm import Category


async def get_category_by_id(db: AsyncSession, category_id: int) -> Category:
    result = await db.execute(select(Category).filter(Category.id == category_id))
    return result.scalars().first()
