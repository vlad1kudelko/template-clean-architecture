from fastapi import HTTPException

from src.modules.base.controller import BaseController
from src.modules.book.schemas import BookRequest, BookResponse


class BookController(BaseController):
    async def create_book(self, book_request: BookRequest) -> BookResponse:
        if len(book_request.authors) != len(set(book_request.authors)):
            raise HTTPException(status_code=422)
        authors = await self.uow.author.get_by_id(book_request.authors)
        if len(book_request.authors) != len(authors):
            raise HTTPException(status_code=404)
        book = await self.uow.book.create_book(
            title=book_request.title,
            genre=book_request.genre,
            author_ids=book_request.authors,
        )
        return BookResponse(
            id=book.id,
            title=book_request.title,
            genre=book_request.genre,
            authors=book_request.authors,
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
