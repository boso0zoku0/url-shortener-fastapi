__all__ = ("db_redis_users", "db_redis_tokens")


import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
)

from dependencies.auth import UNSAFE_METHODS, basic_credentials, validate_basic_auth
from dependencies.short_urls import GetShortUrlsStorage
from schemas.short_url import ShortUrl
from services.auth import db_redis_tokens, db_redis_users

log = logging.getLogger(__name__)

static_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your Static API token from the developer portal",
    auto_error=False,
)


def prefetch_url(slug: str, storage: GetShortUrlsStorage) -> ShortUrl | None:
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"URL {slug!r} not found"
    )


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
        return None
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    return validate_api_token(api_token=api_token)


# вход по username/password(HttpBasic-HTTPBasicCredentials)


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
        return None

    if credentials:
        return validate_basic_auth(credentials=credentials)

    if api_token:
        return validate_api_token(api_token=api_token)

    # ошибка в случае если ни токен ни username/password переданы не были
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token or username and password required",
    )
