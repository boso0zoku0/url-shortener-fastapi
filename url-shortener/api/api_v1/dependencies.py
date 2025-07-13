from typing import Annotated

from schemas.short_url import ShortUrl
from schemas.films import FilmsRead
from api.api_v1.short_urls.crud import storage
from api.api_v1.films.crud import storage as film_storage
from core.config import API_TOKENS, DB_USERS

from fastapi import HTTPException, status, Depends, BackgroundTasks, Request, Header
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)
import logging


log = logging.getLogger(__name__)

static_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your Static API token from the developer portal",
    auto_error=False,
)

basic_credentials = HTTPBasic(
    scheme_name="Basic API token",
    description="Your Basic API token from the developer portal",
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


# вход по токену(HttpBearer-HTTPAuthorizationCredentials)
def validate_by_static_token(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_token)
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API token"
        )


# вход по username/password(HttpBasic-HTTPBasicCredentials)
def basic_auth_validation(
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(basic_credentials)
    ] = None,
):

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User credentials required. Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if (
        credentials
        and credentials.username in DB_USERS
        and DB_USERS[credentials.username] == credentials.password
    ):
        log.info("user is logged %s", credentials.username)
        return
