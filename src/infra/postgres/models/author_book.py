from uuid import UUID

from sqlalchemy import UUID as PGUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.postgres.models.base import Base


class AuthorBook(Base):
    __tablename__ = "authors_books"

    author_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("authors.id"),
        primary_key=True,
    )
    book_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("books.id"),
        primary_key=True,
    )
