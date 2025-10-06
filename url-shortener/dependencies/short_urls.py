from typing import Annotated, Optional

from fastapi import Depends, Request

from core.config import settings
from storage.short_urls import ShortUrlsStorage


def get_short_urls_storage(request: Request) -> Optional[ShortUrlsStorage]:
    return request.app.state.short_urls_storage  # type: ignore[no-any-return]


GetShortUrlsStorage = Annotated[ShortUrlsStorage, Depends(get_short_urls_storage)]
