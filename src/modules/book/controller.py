from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, HTTPException

from src.infra.postgres.uow import PostgresUnitOfWorkDep
from src.modules.base.controller import BaseController
from src.modules.book.schemas import BookRequest, BookResponse


class BookController(BaseController):
    async def create_book(self, body: BookRequest) -> BookResponse:
        if len(body.authors) != len(set(body.authors)):
            raise HTTPException(status_code=422)
        authors = await self.uow.author.get_by_id(body.authors)
        if len(body.authors) != len(authors):
            raise HTTPException(status_code=404)
        book = await self.uow.book.create_book(
            title=body.title,
            genre=body.genre,
            author_ids=body.authors,
        )
        return BookResponse(
            id=book.id,
            title=body.title,
            genre=body.genre,
            authors=body.authors,
        )

    async def read_books(self) -> list[BookResponse]:
        books = await self.uow.book.read_books()
        return [
            BookResponse(
                id=book.id,
                title=book.title,
                genre=book.genre,
                authors=[author.id for author in book.authors],
            )
            for book in books
        ]


async def get_controller(uow: PostgresUnitOfWorkDep) -> AsyncIterator[BookController]:
    yield BookController(uow=uow)


BookControllerDep = Annotated[BookController, Depends(get_controller)]
