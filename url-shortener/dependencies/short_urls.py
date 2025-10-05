from typing import Annotated

from fastapi import Depends, Request

from core.config import settings
from storage.short_urls import ShortUrlsStorage


def get_short_urls_storage(request: Request) -> ShortUrlsStorage:
    return request.app.state.short_urls_storage


GetShortUrlsStorage = Annotated[ShortUrlsStorage, Depends(get_short_urls_storage)]
