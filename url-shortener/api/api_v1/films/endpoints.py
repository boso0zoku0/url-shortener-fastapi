from fastapi import APIRouter, HTTPException, status, Depends
from schemas.films import *
from .crud import storage_films
from ..dependencies import prefetch_url_film

router = APIRouter(prefix="/films", tags=["Films"])


#
@router.get("/", response_model=list[FilmsGet])
def show_films():
    return storage_films.get_films()


@router.post(
    "/create/films/",
    response_model=FilmsCreate | None,
    status_code=status.HTTP_201_CREATED,
)
def create_film(film_create: FilmsCreate):
    return storage_films.create_film(create_films=film_create)


@router.get("/search/{slug}", response_model=FilmsGet)
def search_film_by_slug(slug: str):
    get_film = storage_films.get_by_slug_film(slug=slug)
    if get_film is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {slug} not found"
        )
    return get_film


@router.delete(
    "/delete/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "URL Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not found",
                    }
                }
            },
        },
    },
)
def delete_film(url: Annotated[FilmsGet, Depends(prefetch_url_film)]):
    return storage_films.delete(film_url=url)
