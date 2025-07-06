from schemas.short_url import ShortUrl
from fastapi import HTTPException, status
from .crud import storage


def prefetch_url(slug: str):
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )
