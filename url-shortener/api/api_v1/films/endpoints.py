from fastapi import APIRouter, HTTPException, status
from schemas.films import *
from .crud import storage

router = APIRouter(prefix="/films", tags=["Films"])


#
@router.get("/", response_model=list[FilmsGet])
def show_films():
    return storage.get_films()


@router.post(
    "/create/films/",
    response_model=FilmsCreate | None,
    status_code=status.HTTP_201_CREATED,
)
def create_film(film_create: FilmsCreate):
    return storage.create_film(create_films=film_create)


@router.get("/search/{slug}", response_model=FilmsGet)
def search_film_by_slug(slug: str):
    get_film = storage.get_by_slug_film(slug=slug)
    if get_film is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {slug} not found"
        )
    return get_film
