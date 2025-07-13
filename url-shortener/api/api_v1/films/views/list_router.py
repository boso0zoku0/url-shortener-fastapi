from starlette import status

from api.api_v1.films.crud import storage
from schemas.films import FilmsRead, FilmsCreate

from fastapi import APIRouter, Depends, status
import logging
from api.api_v1.dependencies import (
    validate_by_static_token,
    save_storage_state,
    api_token_or_basic_auth_for_unsafe_methods,
)

log = logging.getLogger(__name__)


router = APIRouter(
    prefix="/films",
    tags=["Films"],
    dependencies=[
        Depends(api_token_or_basic_auth_for_unsafe_methods),
        Depends(save_storage_state),
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


@router.post("/", response_model=FilmsCreate, status_code=status.HTTP_201_CREATED)
def create_film(film_create: FilmsCreate):
    return storage.create_film(create_films=film_create)
