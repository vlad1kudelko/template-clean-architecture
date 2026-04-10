from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.postgres.models.base import MixinId


class BaseStorage[T: MixinId]:
    model_cls: type[T]

    def __init__(self, db: AsyncSession) -> None:
        self._db: AsyncSession = db

    async def get_by_id(self, ids: list[UUID]) -> list[T]:
        stmt = select(self.model_cls).where(self.model_cls.id.in_(ids))
        result = await self._db.execute(stmt)
        return list(result.scalars().all())
