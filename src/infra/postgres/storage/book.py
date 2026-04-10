from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.infra.postgres.models.author import Author
from src.infra.postgres.models.book import Book
from src.infra.postgres.storage.base import BaseStorage


class BookStorage(BaseStorage[Book]):
    model_cls = Book

    async def create_book(self, title: str, genre: str, author_ids: list[UUID]) -> Book:
        stmt = select(Author).where(Author.id.in_(author_ids))
        result = await self._db.execute(stmt)
        authors = result.scalars().all()
        book = Book(title=title, genre=genre, authors=authors)
        await self._db.flush()
        return book

    async def read_books(self) -> Sequence[Book]:
        stmt = select(Book).options(selectinload(Book.authors))
        result = await self._db.execute(stmt)
        return result.scalars().all()
