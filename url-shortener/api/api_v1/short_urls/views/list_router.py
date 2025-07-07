from fastapi import APIRouter
from starlette import status

from api.api_v1.short_urls.crud import storage_short_urls
from schemas.short_url import ShortUrl, ShortUrlCreate

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return storage_short_urls.get()


@router.get("/search")
def search_url(slug: str):
    return storage_short_urls.get_by_slug(slug=slug)


@router.post("/create/", response_model=ShortUrl, status_code=status.HTTP_201_CREATED)
def create_short_url(short_url: ShortUrlCreate):
    return storage_short_urls.create(short_url)
