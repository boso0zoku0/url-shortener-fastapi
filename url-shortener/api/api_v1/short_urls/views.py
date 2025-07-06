from fastapi import HTTPException, status, Request
from rich.json import JSON

from schemas.short_url import *
from fastapi import APIRouter
import random
from api.api_v1.short_urls.crud import SHORT_URLS

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


@router.get("/")
def root(request: Request):
    data = request.url.replace(path="/docs", query="")
    return {"Hello": "Y", "data": data}


@router.post("/", response_model=ShortUrl, status_code=status.HTTP_201_CREATED)
def create_short_url(short_url: Annotated[ShortUrlCreate, JSON]):
    return ShortUrl(id=random.randint(0, 10), **short_url.model_dump())


@router.get("/{slug}/search")
def search_url(slug: str):
    url: ShortUrl = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )
