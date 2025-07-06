from pydantic import BaseModel, AnyHttpUrl

from schemas.short_url import ShortUrl, ShortUrlCreate


class ShortUrlsStorage(BaseModel):
    slug_by_short_urls: dict[str, ShortUrl] = {}

    def get(self) -> list[ShortUrl]:
        return list(self.slug_by_short_urls.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_by_short_urls.get(slug)

    def create(self, short_url_create: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_create.model_dump())
        self.slug_by_short_urls[short_url.slug] = (
            short_url  # обращаемся к slug_by_short_urls и по slug-у short_url сохраняем short_url в словарь
        )
        return short_url


storage = ShortUrlsStorage()

storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("https://www.example.com"),
        slug="example",
    ),
)
storage.create(
    ShortUrlCreate(
        target_url=AnyHttpUrl("https://www.google.com"),
        slug="search",
    ),
)
