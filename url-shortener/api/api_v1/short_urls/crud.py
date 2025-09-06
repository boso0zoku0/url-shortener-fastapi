__all__ = ("storage", "ShortUrlAlreadyExists")

import logging
from collections.abc import Awaitable
from typing import cast

from pydantic import BaseModel
from redis import Redis

from core.config import settings
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlRead,
    ShortUrlUpdate,
    ShortUrlUpdatePartial,
)

log = logging.getLogger(__name__)

redis = Redis(
    host=settings.redis.connect.host,
    port=settings.redis.connect.port,
    db=settings.redis.database.db_redis_short_url,
    decode_responses=True,
)


class ShortUrlBaseError(Exception):
    """
    Base exception for short url CRUD actions
    """


class ShortUrlAlreadyExists(ShortUrlBaseError):
    """
    Raised on short url creation if such slug already exists
    """


class ShortUrlsStorage(BaseModel):
    slug_by_short_urls: dict[str, ShortUrl] = {}

    @classmethod
    def save_short_url(cls, short_url: ShortUrl) -> None:
        redis.hset(
            name=settings.redis.redis_names.redis_short_url_hash_name,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    @classmethod
    def get(cls) -> list[ShortUrlRead]:
        return [
            ShortUrlRead.model_validate_json(value)
            for value in redis.hvals(
                name=settings.redis.redis_names.redis_short_url_hash_name
            )
        ]

    @classmethod
    def get_by_slug(cls, slug: str) -> ShortUrl | None:
        get_db = redis.hget(
            name=settings.redis.redis_names.redis_short_url_hash_name, key=slug
        )
        if get_db:
            return ShortUrl.model_validate_json(get_db)
        return None

    @classmethod
    def exists(cls, slug: str) -> Awaitable[bool] | bool:
        return cast(
            bool,
            redis.hexists(
                name=settings.redis.redis_names.redis_short_url_hash_name, key=slug
            ),
        )

    def create(self, short_url_create: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_create.model_dump())
        self.save_short_url(short_url)
        log.info("Created short url %s", short_url)
        return short_url

    def create_or_raise_if_exists(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        if not self.exists(short_url_in.slug):
            return storage.create(short_url_in)
        raise ShortUrlAlreadyExists(short_url_in.slug)

    @classmethod
    def delete_by_slug(cls, slug: str) -> None:
        redis.hdel(settings.redis.redis_names.redis_short_url_hash_name, slug)
        log.info("Deleted short url %s", slug)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(self, short_url: ShortUrl, short_url_update: ShortUrlUpdate) -> ShortUrl:
        for field_name, value in short_url_update:
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        log.info("Updated short url %s", short_url)
        return short_url

    def update_partial(
        self, short_url: ShortUrl, short_url_update_partial: ShortUrlUpdatePartial
    ) -> ShortUrl:
        for field_name, value in short_url_update_partial.model_dump(
            exclude_unset=True
        ).items():
            setattr(short_url, field_name, value)
        self.save_short_url(short_url)
        log.info("Updated short url %s", short_url)
        return short_url


storage = ShortUrlsStorage()
