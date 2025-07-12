from pydantic import ValidationError

from schemas.short_url import *
from core.config import SHORT_URLS_STORAGE_FILEPATH
import logging

log = logging.getLogger(__name__)


class ShortUrlsStorage(BaseModel):
    slug_by_short_urls: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        for _ in range(30000):
            SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=4))
        log.warning("Saved short urls storage state")

    @classmethod
    def from_state(cls) -> "ShortUrlsStorage":
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            log.warning("No short urls storage found")
            return ShortUrlsStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = ShortUrlsStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error.")
            return

        self.slug_by_short_urls.update(data.slug_by_short_urls)
        log.warning("Recovered data from storage file.")

    def get(self) -> list[ShortUrl]:
        return list(self.slug_by_short_urls.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_by_short_urls.get(slug)

    def create(self, short_url_create: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_create.model_dump())
        self.slug_by_short_urls[short_url.slug] = short_url
        # self.save_state()
        log.warning("Created short url %s", short_url)
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_by_short_urls.pop(slug, None)
        # self.save_state()
        log.info("Deleted short url %s", slug)

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(self, short_url: ShortUrl, short_url_update: ShortUrlUpdate) -> ShortUrl:
        for field_name, value in short_url_update:
            setattr(short_url, field_name, value)
        # self.save_state()
        log.info("Updated short url %s", short_url)
        return short_url

    def update_partial(
        self, short_url: ShortUrl, short_url_update_partial: ShortUrlUpdatePartial
    ) -> ShortUrl:
        for field_name, value in short_url_update_partial.model_dump(
            exclude_unset=True
        ).items():
            setattr(short_url, field_name, value)
        # self.save_state()
        log.info("Updated short url %s", short_url)
        return short_url


storage = ShortUrlsStorage()
