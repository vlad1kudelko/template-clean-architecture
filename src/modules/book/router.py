from fastapi import APIRouter

from src.modules.book.controller import BookControllerDep
from src.modules.book.schemas import BookRequest, BookResponse

router = APIRouter(prefix="/books")


@router.get("/")
async def get(controller: BookControllerDep) -> list[BookResponse]:
    return await controller.read_books()


@router.post("/")
async def post(controller: BookControllerDep, body: BookRequest) -> BookResponse:
    return await controller.create_book(body)
