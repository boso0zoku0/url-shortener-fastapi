from typing import Annotated

from schemas.short_url import ShortUrl
from schemas.films import FilmsRead
from api.api_v1.short_urls.crud import storage
from api.api_v1.films.crud import storage as film_storage
from core.config import API_TOKENS

from fastapi import HTTPException, status, Depends, BackgroundTasks, Request, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import logging


log = logging.getLogger(__name__)

static_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your Static API token from the developer portal",
    auto_error=False,
)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)


def prefetch_url(slug: str):
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


def prefetch_url_film(slug: str):
    url: FilmsRead | None = film_storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {slug!r} not found"
    )


#
def get_film_by_slug_exc(slug: str = Depends(film_storage.get_by_slug)):
    if slug is None:
        raise HTTPException(status_code=404, detail=f"Slug by Film: {slug} not found")
    return slug


def save_storage_state(
    background_tasks: BackgroundTasks,
    request: Request,
):

    yield
    if request.method in UNSAFE_METHODS:
        log.info("method: %s", request.method)
        log.info("Add background task to save storage")
        background_tasks.add_task(storage.save_state)
    return


def api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_token)
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return
    # if api_token not in API_TOKENS:
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API token"
        )


# def api_token_required(
#     request: Request,
#     api_token: Annotated[
#         HTTPAuthorizationCredentials | None,
#         Depends(static_token),
#     ] = None,
# ):
#     if request.method not in UNSAFE_METHODS:
#         return
#
#     if not api_token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="API token is required",
#         )

# if api_token.credentials not in API_TOKENS:
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid API token",
#     )
