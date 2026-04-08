
```bash
docker compose build app ; docker compose run --rm app sh -c \
    "uv run alembic revision --autogenerate ; cat /app/src/infra/postgres/alembic/versions/*"
```
