from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.app_config import app_config

engine: AsyncEngine = create_async_engine(app_config.url)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


@asynccontextmanager
async def get_db() -> AsyncIterator[AsyncSession]:
    async with session_factory() as db:
        try:
            yield db
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()
