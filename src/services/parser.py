import asyncio

from services.gpc_client import GPCClient


async def fetch_categories() -> list:
    client = GPCClient()

    segments_task = client.fetch("segment")
    families_task = client.fetch("family")
    classes_task = client.fetch("class")

    segments, families, classes = await asyncio.gather(
        segments_task, families_task, classes_task
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
            normalize(classes)
    )

    return result
