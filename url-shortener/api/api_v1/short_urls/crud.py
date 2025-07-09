# from pydantic import BaseModel
from pydantic import ValidationError

from schemas.short_url import *
from core.config import SHORT_URLS_STORAGE_FILEPATH


class ShortUrlsStorage(BaseModel):
    slug_by_short_urls: dict[str, ShortUrl] = {}

    def save_state(self) -> None:
        SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=4))

    @classmethod
    def from_state(cls) -> "ShortUrlsStorage":
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            return ShortUrlsStorage()
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())

    def get(self) -> list[ShortUrl]:
        return list(self.slug_by_short_urls.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_by_short_urls.get(slug)

    def create(self, short_url_create: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_create.model_dump())
        self.slug_by_short_urls[short_url.slug] = (
            short_url  # обращаемся к slug_by_short_urls и по slug-у short_url сохраняем short_url в словарь
        )
        self.save_state()
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_by_short_urls.pop(slug, None)
        self.save_state()

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(self, short_url: ShortUrl, short_url_update: ShortUrlUpdate) -> ShortUrl:
        for field_name, value in short_url_update:
            setattr(short_url, field_name, value)
        self.save_state()
        return short_url

    def update_partial(
        self, short_url: ShortUrl, short_url_update_partial: ShortUrlUpdatePartial
    ) -> ShortUrl:
        for field_name, value in short_url_update_partial.model_dump(
            exclude_unset=True
        ).items():
            setattr(short_url, field_name, value)
        self.save_state()
        return short_url


try:
    storage = ShortUrlsStorage.from_state()
except ValidationError:
    storage = ShortUrlsStorage()
    storage.save_state()
# storage = ShortUrlsStorage()
# try:
#     storage = ShortUrlsStorage().from_state()
#
# except ValidationError:
#     storage = ShortUrlsStorage()


# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("https://www.example.com"),
#         slug="example",
#     ),
# )
# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("https://www.google.com"),
#         slug="search",
#     ),
# )
