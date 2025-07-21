from fastapi import HTTPException, status
from pydantic import ValidationError
from redis import Redis

from schemas.short_url import *
from core import config
import logging

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_SHORT_URLS,
    decode_responses=True,
)


class ShortUrlsStorage(BaseModel):
    slug_by_short_urls: dict[str, ShortUrl] = {}

    def save_short_url(self, short_url: ShortUrl) -> None:
        redis.hset(
            name=config.REDIS_SHORT_URLS_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    def get(self):
        return [
            ShortUrlRead.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_SHORT_URLS_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        get_db = redis.hget(name=config.REDIS_SHORT_URLS_HASH_NAME, key=slug)
        if get_db:
            return ShortUrl.model_validate_json(get_db)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Short url not found %s"
        )

    def create(self, short_url_create: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_create.model_dump())
        self.save_short_url(short_url)
        log.warning("Created short url %s", short_url)
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(config.REDIS_SHORT_URLS_HASH_NAME, slug)
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
