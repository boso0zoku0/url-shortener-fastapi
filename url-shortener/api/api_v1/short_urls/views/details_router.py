from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from api.api_v1.dependencies import prefetch_url
from api.api_v1.short_urls.crud import storage_short_urls
from schemas.short_url import ShortUrl


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


@router.get("/")
def redirect(url: Annotated[ShortUrl, Depends(prefetch_url)]):
    return url


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_slug(url: Annotated[ShortUrl, Depends(prefetch_url)]):
    return storage_short_urls.delete(short_url=url)
