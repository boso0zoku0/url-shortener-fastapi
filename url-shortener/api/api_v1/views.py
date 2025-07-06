from fastapi import HTTPException, status, Request
from schemas.short_url import ShortUrl
from fastapi import APIRouter

from .short_urls.crud import SHORT_URLS

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


@router.get("/")
def root(request: Request):
    data = request.url.replace(path="/docs", query="")
    return {"Hello": "Y", "data": data}


@router.get("/{slug}/search")
def search_url(slug: str):
    url: ShortUrl = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )
