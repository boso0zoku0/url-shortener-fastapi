from schemas.short_url import ShortUrl
from schemas.films import FilmsGet
from fastapi import HTTPException, status
from api.api_v1.short_urls.crud import storage_short_urls
from api.api_v1.films.crud import storage_films


def prefetch_url(slug: str):
    url: ShortUrl | None = storage_short_urls.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


def prefetch_url_film(slug: str):
    url: FilmsGet | None = storage_films.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )
