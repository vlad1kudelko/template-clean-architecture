from sqlalchemy.orm import Mapped, relationship

from src.infra.postgres.models.base import Base, MixinId


class Book(Base, MixinId):
    __tablename__ = "books"

    title: Mapped[str]
    genre: Mapped[str]

    authors: Mapped[list["Author"]] = relationship("Author", secondary="authors_books", back_populates="books")
