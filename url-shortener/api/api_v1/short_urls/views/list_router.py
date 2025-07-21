from fastapi import APIRouter, HTTPException, status, Depends

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead
from api.api_v1.auth.services.redis_tokens_helper import db_redis_tokens
from api.api_v1.dependencies import (
    api_token_or_basic_auth_for_unsafe_methods,
)


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


# @router.post("/add-token")
# def generate_and_save_token(token: str):
#     return db_redis_tokens.generate_and_save_token(token)
#


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
                        "detail": "Short Url with slug='foobar' already exists.",
                    },
                },
            },
        },
    },
)
def create_short_url(short_url: ShortUrlCreate):
    if not storage.get_by_slug(short_url.slug):
        return storage.create(short_url)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Such a short link {short_url.slug!r} already exists",
    )


@router.get("/search", response_model=ShortUrlRead)
def search_url(slug: str):
    return storage.get_by_slug(slug=slug)


@router.post("/add-token", status_code=status.HTTP_201_CREATED)
def add_token(token):
    return db_redis_tokens.add_token(token)
