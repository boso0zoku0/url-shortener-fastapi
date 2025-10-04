__all__ = ("storage",)

import logging
from collections.abc import Awaitable
from typing import cast, Iterable

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
from storage.short_urls.exceptions import ShortUrlAlreadyExists

log = logging.getLogger(__name__)

redis = Redis(
    host=settings.redis.connect.host,
    port=settings.redis.connect.port,
    db=settings.redis.database.db_redis_short_url,
    decode_responses=True,
)


class ShortUrlsStorage(BaseModel):
    slug_by_short_urls: dict[str, ShortUrl] = {}
    name_db: str

    def save_short_url(self, short_url: ShortUrl) -> None:
        redis.hset(
            name=self.name_db,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    def get(self) -> list[ShortUrlRead]:
        return [
            ShortUrlRead.model_validate_json(value)
            for value in cast(
                Iterable[str],
                redis.hvals(
                    name=self.name_db,
                ),
            )
        ]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        if data := redis.hget(
            name=self.name_db,
            key=slug,
        ):
            assert isinstance(data, str)
            return ShortUrl.model_validate_json(data)

        return None

    def exists(self, slug: str) -> Awaitable[bool] | bool:
        return cast(
            bool,
            redis.hexists(name=self.name_db, key=slug),
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

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(self.name_db, slug)
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


storage = ShortUrlsStorage(name_db=settings.redis.redis_names.redis_short_url_hash_name)
