from fastapi import status

from schemas.short_url import *
from fastapi import APIRouter
from .crud import storage

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return storage.get()


@router.post("/create/", response_model=ShortUrl, status_code=status.HTTP_201_CREATED)
def create_short_url(short_url: ShortUrlCreate):
    return storage.create(short_url)


@router.get("/{slug}/search")
def search_url(slug: str):
    return storage.get_by_slug(slug=slug)
