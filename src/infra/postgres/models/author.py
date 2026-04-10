from uuid import UUID

from sqlalchemy import UUID as PGUUID, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.postgres.models.base import Base, MixinId


class Author(Base, MixinId):
    __tablename__ = "authors"

    name: Mapped[str]

    authors_books: Mapped[list["AuthorBook"]] = relationship("AuthorBook", back_populates="authors")
    books: Mapped[list["Book"]] = relationship("Book", secondary="authors_books", back_populates="authors")
