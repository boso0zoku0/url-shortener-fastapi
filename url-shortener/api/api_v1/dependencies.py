from schemas.short_url import ShortUrl
from schemas.films import FilmsRead
from fastapi import HTTPException, status, Depends
from api.api_v1.short_urls.crud import storage
from api.api_v1.films.crud import storage


def prefetch_url(slug: str):
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


def prefetch_url_film(slug: str):
    url: FilmsRead | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


def get_film_by_slug_exc(slug=Depends(storage.get_by_slug)):
    if slug is None:
        raise HTTPException(status_code=404, detail=f"Film {slug} not found")
    return slug
