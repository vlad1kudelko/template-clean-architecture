from src.infra.postgres.models.author import Author
from src.infra.postgres.storage.base import BaseStorage


class AuthorStorage(BaseStorage[Author]):
    model_cls = Author
