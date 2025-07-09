from fastapi import APIRouter
from starlette import status

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


@router.get("/", response_model=list[ShortUrlRead])
def read_short_urls_list() -> list[ShortUrl]:
    return storage.get()


@router.get("/search", response_model=ShortUrlRead)
def search_url(slug: str):
    return storage.get_by_slug(slug=slug)


@router.post(
    "/create/", response_model=ShortUrlRead, status_code=status.HTTP_201_CREATED
)
def create_short_url(short_url: ShortUrlCreate):
    return storage.create(short_url)
