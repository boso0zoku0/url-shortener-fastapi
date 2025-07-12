from starlette import status

from api.api_v1.films.crud import storage
from schemas.films import FilmsRead, FilmsCreate

from fastapi import APIRouter, BackgroundTasks, Depends
import logging

log = logging.getLogger(__name__)
router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=list[FilmsRead])
def show_films():
    return storage.get_films()


def spam_log():
    log.info("spam log")


@router.post("/", response_model=FilmsCreate, status_code=status.HTTP_201_CREATED)
def create_film(
    film_create: FilmsCreate,
    background_tasks: BackgroundTasks,
    _=Depends(spam_log),
):
    background_tasks.add_task(storage.save_state)
    return storage.create_film(create_films=film_create)
