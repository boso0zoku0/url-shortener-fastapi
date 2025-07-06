from fastapi import status, Depends

from schemas.short_url import *
from fastapi import APIRouter
from .crud import storage_short_urls
from ..dependencies import prefetch_url

router = APIRouter(prefix="/short-urls", tags=["Short URLs"])


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return storage_short_urls.get()


@router.post("/create/", response_model=ShortUrl, status_code=status.HTTP_201_CREATED)
def create_short_url(short_url: ShortUrlCreate):
    return storage_short_urls.create(short_url)


@router.get("/{slug}/search")
def search_url(slug: str):
    return storage_short_urls.get_by_slug(slug=slug)


@router.delete(
    "/delete/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
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
def delete_by_slug(url: Annotated[ShortUrl, Depends(prefetch_url)]):
    return storage_short_urls.delete(short_url=url)
