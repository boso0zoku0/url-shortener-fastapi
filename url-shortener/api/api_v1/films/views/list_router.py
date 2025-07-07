from starlette import status

from api.api_v1.films.crud import storage_films
from schemas.films import FilmsGet, FilmsCreate

from fastapi import APIRouter

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=list[FilmsGet])
def show_films():
    return storage_films.get_films()


@router.post(
    "/create/",
    response_model=FilmsCreate | None,
    status_code=status.HTTP_201_CREATED,
)
def create_film(film_create: FilmsCreate):
    return storage_films.create_film(create_films=film_create)
