from starlette import status

from api.api_v1.films.crud import storage
from schemas.films import FilmsRead, FilmsCreate

from fastapi import APIRouter, BackgroundTasks, Depends
import logging
from api.api_v1.dependencies import save_storage_state

log = logging.getLogger(__name__)
router = APIRouter(
    prefix="/films", tags=["Films"], dependencies=[Depends(save_storage_state)]
)


# def write_notification(email: str, message=""):
#     with open("log.txt", mode="w") as email_file:
#         content = f"notification for {email}: {message}"
#         email_file.write(content)


@router.get("/", response_model=list[FilmsRead])
def show_films(_=Depends(save_storage_state)):
    return storage.get_films()


@router.post("/", response_model=FilmsCreate, status_code=status.HTTP_201_CREATED)
def create_film(film_create: FilmsCreate, _=Depends(save_storage_state)):
    return storage.create_film(create_films=film_create)
