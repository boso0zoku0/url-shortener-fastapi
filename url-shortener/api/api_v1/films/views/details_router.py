from typing import Annotated

from fastapi import Depends
from starlette import status

from api.api_v1.dependencies import prefetch_url_film, get_film_by_slug_exc
from api.api_v1.films.crud import storage_films
from schemas.films import FilmsGet, FilmsUpdate, FilmsUpdatePartial
from fastapi import APIRouter

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Film not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Film by 'slug' not found",
                    }
                }
            },
        },
    },
)

FilmBySlug = Annotated[FilmsGet, Depends(prefetch_url_film)]


@router.get("/", response_model=FilmsGet)
def search_film_by_slug(slug=Depends(storage_films.get_by_slug)):
    return get_film_by_slug_exc(slug)


@router.delete(
    "/",
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


@router.put("/", response_model=FilmsGet)
def put_film(film: FilmBySlug, film_update: FilmsUpdate) -> FilmsGet:
    return storage_films.update(film=film, film_update=film_update)


@router.patch("/", response_model=FilmsGet)
def patch_film(film: FilmBySlug, film_update: FilmsUpdatePartial) -> FilmsGet:
    return storage_films.update_partial(film=film, film_update_partial=film_update)
