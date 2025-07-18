from typing import Annotated

# from core import config
# from redis_db import rediss


from api.api_v1.redis_db import redis as db_redis
from schemas.short_url import ShortUrl
from schemas.films import FilmsRead
from api.api_v1.short_urls.crud import storage
from api.api_v1.films.crud import storage as film_storage
from core.config import DB_USERS
from fastapi import HTTPException, status, Depends, BackgroundTasks, Request
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


def validate_api_token(api_token: HTTPAuthorizationCredentials):
    if db_redis.token_exists(token=api_token.credentials):
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API token"
    )


# def validate_api_token(api_token: HTTPAuthorizationCredentials):
#     if api_token.credentials:
#         return
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API token"
#     )


# вход по токену(HttpBearer-HTTPAuthorizationCredentials)
def validate_by_static_token(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_token)
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    validate_api_token(api_token=api_token)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if (
        credentials
        and credentials.username in DB_USERS
        and DB_USERS[credentials.username] == credentials.password
    ):
        log.info("user is logged %s", credentials.username)
        return


# вход по username/password(HttpBasic-HTTPBasicCredentials)
def basic_auth_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(basic_credentials)
    ] = None,
):

    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(credentials)


def api_token_or_basic_auth_for_unsafe_methods(
    request: Request,
    api_token: Annotated[HTTPAuthorizationCredentials, Depends(static_token)],
    credentials: Annotated[HTTPBasicCredentials, Depends(basic_credentials)],
):
    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        return validate_basic_auth(credentials=credentials)

    if api_token:
        return validate_api_token(api_token=api_token)

    # ошибка в случае если ни токен ни username/password переданы не были
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token or username and password required",
    )
