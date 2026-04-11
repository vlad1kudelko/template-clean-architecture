from uuid import UUID

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    genre: str
    authors: list[UUID]


class BookRequest(BookBase): ...


class BookResponse(BookBase):
    id: UUID
