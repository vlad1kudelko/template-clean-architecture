from dataclasses import dataclass

from src.infra.postgres.uow import PostgresUnitOfWork


@dataclass
class BaseController:
    uow: PostgresUnitOfWork
