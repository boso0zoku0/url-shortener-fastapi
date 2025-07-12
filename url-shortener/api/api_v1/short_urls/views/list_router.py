from fastapi import APIRouter
from starlette import status

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead
from fastapi import BackgroundTasks

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


@router.get("/read-urls", response_model=list[ShortUrl])
def read_short_urls_list() -> list[ShortUrlRead]:
    return storage.get()


@router.post("/", response_model=ShortUrlRead, status_code=status.HTTP_201_CREATED)
def create_short_url(short_url: ShortUrlCreate, background_tasks: BackgroundTasks):
    background_tasks.add_task(storage.save_state)
    return storage.create(short_url)


@router.get("/search", response_model=ShortUrlRead)
def search_url(slug: str):
    return storage.get_by_slug(slug=slug)
