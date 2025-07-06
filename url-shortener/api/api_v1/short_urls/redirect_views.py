from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from schemas.short_url import ShortUrl
from api.api_v1.short_urls.dependencies import prefetch_url

router = APIRouter(prefix="/r", tags=["Redirect"])


@router.get("/{slug}")
def redirect(url: Annotated[ShortUrl, Depends(prefetch_url)]):
    return url
