from fastapi import APIRouter
from starlette import status

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead
from fastapi import Depends
from api.api_v1.redis_db import redis as db_redis
from api.api_v1.dependencies import (
    save_storage_state,
    api_token_or_basic_auth_for_unsafe_methods,
)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[
        Depends(api_token_or_basic_auth_for_unsafe_methods),
        Depends(save_storage_state),
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


@router.post("/add-token")
def generate_and_save_token(token: str):
    return db_redis.generate_and_save_token(token)


@router.get("/read-urls", response_model=list[ShortUrl])
def read_short_urls_list() -> list[ShortUrlRead]:
    return storage.get()


@router.post("/", response_model=ShortUrlRead, status_code=status.HTTP_201_CREATED)
def create_short_url(short_url: ShortUrlCreate):
    return storage.create(short_url)


@router.get("/search", response_model=ShortUrlRead)
def search_url(slug: str):
    return storage.get_by_slug(slug=slug)


@router.post("/add-token", status_code=status.HTTP_201_CREATED)
def add_token(token):
    return db_redis.add_token(token)
