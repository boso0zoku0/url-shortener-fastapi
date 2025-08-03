from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from schemas.short_url import ShortUrl

from api.api_v1.dependencies import prefetch_url

router = APIRouter(
    prefix="/r",
    tags=["Redirect"],
)


@router.get("/{slug}")
@router.get("/{slug}/")
def redirect_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_url),
    ],
) -> RedirectResponse:
    return RedirectResponse(
        url=str(url.target_url),
    )
