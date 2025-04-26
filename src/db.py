from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from models.orm import Base
from settings import settings

engine = create_async_engine(settings.db.url, echo=settings.debug)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
