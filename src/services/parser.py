import asyncio

from db import new_session
from models.orm import Category
from services.gpc_client import GPCClient
from sqlalchemy.dialects.postgresql import insert as pg_insert


async def fetch_categories() -> list:
    client = GPCClient()

    segments_task = client.fetch("segment")
    families_task = client.fetch("family")
    classes_task = client.fetch("class")
    bricks_task = client.fetch("brick")

    segments, families, classes, bricks = await asyncio.gather(
        segments_task, families_task, classes_task, bricks_task
    )

    def normalize(items: list) -> list:
        return [
            {
                "id": item.get("code"),
                "parent_id": item.get("parentCode"),
                "title": item.get("title"),
                "description": item.get("definition"),
            }
            for item in items
        ]

    result = (
            normalize(segments) +
            normalize(families) +
            normalize(classes) +
            normalize(bricks)
    )

    return result


async def save_categories(categories: list):
    async with new_session() as session:
        stmt = pg_insert(Category).values(categories)
        update_stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={
                c.name: getattr(stmt.excluded, c.name)
                for c in Category.__table__.columns
                if c.name != "id"
            }
        )

        await session.execute(update_stmt)
        await session.commit()
