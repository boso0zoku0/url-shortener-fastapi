from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.dependencies import prefetch_url
from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlRead,
    ShortUrlUpdate,
    ShortUrlUpdatePartial,
)

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Short URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'stug' not found",
                    }
                }
            },
        },
    },
)

ShortUrlBySlug = Annotated[ShortUrl, Depends(prefetch_url)]


@router.get("/", response_model=ShortUrlRead)
def get_short_url_by_slug(slug: str) -> ShortUrl | None:
    return storage.get_by_slug(slug)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_slug(url: ShortUrlBySlug) -> None:
    return storage.delete(short_url=url)


@router.put("/", response_model=ShortUrlRead)
def put_short_url(
    url: ShortUrlBySlug,
    short_url_update: ShortUrlUpdate,
) -> ShortUrl:
    return storage.update(short_url=url, short_url_update=short_url_update)


@router.patch("/", response_model=ShortUrlRead)
def patch_short_url(
    url: ShortUrlBySlug,
    short_url_update_partial: ShortUrlUpdatePartial,
) -> ShortUrl:
    return storage.update_partial(
        short_url=url, short_url_update_partial=short_url_update_partial
    )
