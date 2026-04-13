from httpx import AsyncClient

from tests.conftest import AUTHOR_1, AUTHOR_2

AUTHOR_NONE = "33333333-3b61-4667-9a7c-61acb3d132f1"


async def test_get_books_returns_list(client: AsyncClient):
    resp = await client.get("/api/books/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


async def test_create_book_returns_correct_fields(client: AsyncClient):
    payload = {
        "title": "Title book",
        "genre": "Novel",
        "authors": [AUTHOR_1],
    }
    resp = await client.post("/api/books/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["title"] == "Title book"
    assert data["genre"] == "Novel"
    assert AUTHOR_1 in data["authors"]


async def test_created_book_appears_in_list(client: AsyncClient):
    payload = {
        "title": "1984",
        "genre": "Dystopian",
        "authors": [AUTHOR_2],
    }
    create_resp = await client.post("/api/books/", json=payload)
    assert create_resp.status_code == 200
    created_id = create_resp.json()["id"]
    list_resp = await client.get("/api/books/")
    assert list_resp.status_code == 200
    ids = [b["id"] for b in list_resp.json()]
    assert created_id in ids


async def test_create_book_with_multiple_authors(client: AsyncClient):
    payload = {
        "title": "Co-authored Book",
        "genre": "Fiction",
        "authors": [AUTHOR_1, AUTHOR_2],
    }
    resp = await client.post("/api/books/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["authors"]) == 2
    assert AUTHOR_1 in data["authors"]
    assert AUTHOR_2 in data["authors"]


async def test_create_book_with_none_author_returns_error(client: AsyncClient):
    payload = {
        "title": "Book with missing author",
        "genre": "Test",
        "authors": [AUTHOR_NONE],
    }
    resp = await client.post("/api/books/", json=payload)
    assert resp.status_code == 404


async def test_create_book_with_duplicate_authors_returns_error(client: AsyncClient):
    payload = {
        "title": "Book with duplicate authors",
        "genre": "Test",
        "authors": [AUTHOR_1, AUTHOR_1],
    }
    resp = await client.post("/api/books/", json=payload)
    assert resp.status_code == 422
