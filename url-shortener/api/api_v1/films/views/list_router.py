from api.api_v1.films.crud import storage
from schemas.films import FilmsRead, FilmsCreate

from fastapi import APIRouter, Depends, status, HTTPException
import logging
from api.api_v1.dependencies import api_token_or_basic_auth_for_unsafe_methods

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

# def write_notification(email: str, message=""):
#     with open("log.txt", mode="w") as email_file:
#         content = f"notification for {email}: {message}"
#         email_file.write(content)


@router.get("/", response_model=list[FilmsRead])
def show_films():
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
                        "detail": "Film with slug='foobar' already exists.",
                    },
                },
            },
        },
    },
)
def create_film(film_create: FilmsCreate):
    if not storage.get_by_slug(slug=film_create.slug):
        return storage.create_film(create_films=film_create)
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Such a short link {film_create.slug!r} already exists",
    )
