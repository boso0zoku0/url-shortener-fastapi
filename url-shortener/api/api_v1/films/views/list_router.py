from starlette import status

from api.api_v1.films.crud import storage
from schemas.films import FilmsRead, FilmsCreate

from fastapi import APIRouter

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=list[FilmsRead])
def show_films():
    return storage.get_films()


@router.post(
    "/create/",
    response_model=FilmsCreate | None,
    status_code=status.HTTP_201_CREATED,
)
def create_film(film_create: FilmsCreate):
    return storage.create_film(create_films=film_create)
