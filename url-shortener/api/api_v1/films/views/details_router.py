from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status

from api.api_v1.dependencies import prefetch_url_film
from api.api_v1.films.crud import storage_films
from schemas.films import FilmsGet
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


@router.get("/search/", response_model=FilmsGet)
def search_film_by_slug(slug: str):
    get_film = storage_films.get_by_slug(slug=slug)
    if get_film is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {slug} not found"
        )
    return get_film


@router.delete(
    "/delete/",
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
