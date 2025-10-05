from typing import Annotated

from fastapi import Depends

from core.config import settings
from storage.short_urls import ShortUrlsStorage


def get_short_urls_storage() -> ShortUrlsStorage:
    return ShortUrlsStorage(
        name_db=settings.redis.redis_names.redis_short_url_hash_name
    )


GetShortUrlsStorage = Annotated[ShortUrlsStorage, Depends(get_short_urls_storage)]
