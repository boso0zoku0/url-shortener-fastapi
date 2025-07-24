__all__ = "db_redis_users"


from typing import Annotated

from api.api_v1.auth.services.redis_users_helper import db_redis_users
from api.api_v1.auth.services.redis_tokens_helper import db_redis_tokens
from schemas.short_url import ShortUrl
from schemas.film import FilmsRead
from api.api_v1.short_urls.crud import storage
from api.api_v1.films.crud import storage as film_storage

from fastapi import HTTPException, status, Depends, Request
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


def prefetch_url(slug: str) -> ShortUrl | None:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


def prefetch_url_film(slug: str) -> FilmsRead | None:
    url: FilmsRead | None = film_storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Film {slug!r} not found"
    )


#
def get_film_by_slug_exc(
    slug: FilmsRead | None = Depends(film_storage.get_by_slug),
) -> FilmsRead | None:
    if not slug:
        raise HTTPException(status_code=404, detail=f"Slug by Film: {slug} not found")
    return slug


def validate_api_token(api_token: HTTPAuthorizationCredentials) -> None:
    if db_redis_tokens.token_exists(token=api_token.credentials):
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API token"
    )


# вход по токену(HttpBearer-HTTPAuthorizationCredentials)
def validate_by_static_token(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_token)
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHODS:
        return
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    return validate_api_token(api_token=api_token)


def validate_basic_auth(credentials: HTTPBasicCredentials | None) -> None:
    if credentials and db_redis_users.validate_user_password(
        username=credentials.username, password=credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


# вход по username/password(HttpBasic-HTTPBasicCredentials)
def basic_auth_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(basic_credentials)
    ] = None,
) -> None:

    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(credentials)


def api_token_or_basic_auth_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_token)
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(basic_credentials)
    ] = None,
) -> None:
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
