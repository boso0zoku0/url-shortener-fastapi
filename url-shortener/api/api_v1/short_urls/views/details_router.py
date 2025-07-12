from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status

from api.api_v1.dependencies import prefetch_url
from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlUpdate,
    ShortUrlUpdatePartial,
    ShortUrlRead,
    ShortUrlCreate,
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

ShortUrlBySlug = Annotated[ShortUrlCreate, Depends(prefetch_url)]


@router.get("/")
def redirect(url: ShortUrlBySlug):
    return url


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_slug(url: ShortUrlBySlug, background_tasks: BackgroundTasks) -> None:
    background_tasks.add_task(storage.save_state)
    return storage.delete(short_url=url)


@router.put("/", response_model=ShortUrlRead)
def put_short_url(
    url: ShortUrlBySlug,
    short_url_update: ShortUrlUpdate,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(storage.save_state)
    return storage.update(short_url=url, short_url_update=short_url_update)


@router.patch("/", response_model=ShortUrlRead)
def patch_short_url(
    url: ShortUrlBySlug,
    short_url_update_partial: ShortUrlUpdatePartial,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(storage.save_state)
    return storage.update_partial(
        short_url=url, short_url_update_partial=short_url_update_partial
    )
