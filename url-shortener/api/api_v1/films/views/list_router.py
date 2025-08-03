import logging

from fastapi import APIRouter, Depends, HTTPException, status

from api.api_v1.dependencies import api_token_or_basic_auth_for_unsafe_methods
from api.api_v1.films.crud import FilmsAlreadyExistsError, storage
from schemas.film import FilmsCreate, FilmsRead

log = logging.getLogger(__name__)


router = APIRouter(
    prefix="/films",
    tags=["Films"],
    dependencies=[
        Depends(api_token_or_basic_auth_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid API token"},
                }
            },
        },
    },
)


@router.get("/")
def show_films() -> list[FilmsRead]:
    return storage.get_films()


@router.post(
    "/",
    response_model=FilmsCreate,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Conflict. Duplicate entries are not allowed.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Film with slug='name' already exists.",
                    },
                },
            },
        },
    },
)
def create_film(film_create: FilmsCreate) -> FilmsRead | None:
    try:
        return storage.create_or_raise_if_exists(film_create)
    except FilmsAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Film with slug={film_create.slug} already exists",
        )
