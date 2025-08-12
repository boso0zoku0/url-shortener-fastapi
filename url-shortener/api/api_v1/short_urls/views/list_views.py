import logging

from fastapi import APIRouter, Depends, HTTPException, status

from api.api_v1.auth.services.redis_tokens_helper import db_redis_tokens
from api.api_v1.dependencies import (
    api_token_or_basic_auth_for_unsafe_methods,
)
from api.api_v1.short_urls.crud import ShortUrlAlreadyExists, storage
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[
        Depends(api_token_or_basic_auth_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


@router.get("/read-urls", response_model=list[ShortUrl])
def read_short_urls_list() -> list[ShortUrlRead]:
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Conflict. Duplicate entries are not allowed.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Short Url with slug='name' already exists.",
                    },
                },
            },
        },
    },
)
def create_short_url(short_url_in: ShortUrlCreate) -> ShortUrl:
    try:
        return storage.create_or_raise_if_exists(short_url_in)
    except ShortUrlAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Short URL with slug = {short_url_in.slug} already exists",
        )


@router.get("/search", response_model=ShortUrlRead)
def search_url(slug: str) -> ShortUrl | None:
    return storage.get_by_slug(slug=slug)


@router.post("/add-token", status_code=status.HTTP_201_CREATED)
def add_token(token: str) -> None:
    return db_redis_tokens.add_token(token)


@router.post("/transfer")
def transfer_short_url() -> dict[str, str]:
    return {"hello": "world"}
    # raise ValueError
