from fastapi import APIRouter
from typing import Annotated
from fastapi import HTTPException, Depends, status, Request
from starlette.responses import RedirectResponse
from schemas.short_url import ShortUrl
from .short_urls.dependencies import prefetch_url

router = APIRouter(prefix="/r", tags=["Redirect"])


@router.get("/{slug}")
def redirect(url: Annotated[ShortUrl, Depends(prefetch_url)]):
    return url
