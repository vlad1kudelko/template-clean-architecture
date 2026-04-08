from uuid import UUID

from sqlalchemy import UUID as PGUUID
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.postgres.models.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    title: Mapped[str]
    genre: Mapped[str]

    authors_books: Mapped["AuthorBook"] = relationship("AuthorBook", back_populates="books")
    authors: Mapped["Author"] = relationship("Author", secondary="authors_books", back_populates="books")
