from typing import Annotated

from fastapi import Depends
from starlette import status

from api.api_v1.dependencies import prefetch_url_film, get_film_by_slug_exc
from api.api_v1.films.crud import storage
from schemas.films import FilmsRead, FilmsUpdate, FilmsUpdatePartial
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

FilmBySlug = Annotated[FilmsRead, Depends(prefetch_url_film)]


@router.get("/", response_model=FilmsRead)
def search_film_by_slug(slug=Depends(storage.get_by_slug)):
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
def delete_film(url: Annotated[FilmsRead, Depends(prefetch_url_film)]) -> None:
    return storage.delete(film_url=url)


@router.put("/", response_model=FilmsRead)
def put_film(film: FilmBySlug, film_update: FilmsUpdate) -> FilmsRead:
    return storage.update(film=film, film_update=film_update)


@router.patch("/", response_model=FilmsRead)
def patch_film(film: FilmBySlug, film_update: FilmsUpdatePartial) -> FilmsRead:
    return storage.update_partial(film=film, film_update_partial=film_update)
