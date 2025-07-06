from schemas.short_url import ShortUrl
from starlette.responses import RedirectResponse
from fastapi import HTTPException, status
from .crud import SHORT_URLS


def prefetch_url(slug: str):
    url: ShortUrl = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return RedirectResponse(url=url.target_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )
