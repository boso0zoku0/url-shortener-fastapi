import string
from random import choices
from unittest import TestCase

from os import getenv

from api.api_v1.short_urls.crud import storage
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlUpdatePartial,
)

if getenv("TESTING") != "1":
    raise EnvironmentError("Environment variable TESTING must be 1")


class ShortUrlUpdateTestCase(TestCase):

    def setUp(self) -> None:
        self.short_url = self.create_short_url()

    def tearDown(self) -> None:
        storage.delete(self.short_url)

    def create_short_url(self) -> ShortUrl:

        short_url = ShortUrlCreate(
            target_url="https://example.com",
            description="A short url",
            slug="".join(choices(string.ascii_letters, k=8)),
        )

        return storage.create(short_url)

    def test_update(self) -> None:
        short_url_update = ShortUrlUpdate(**self.short_url.model_dump())
        source_description = short_url_update.description
        short_url_update.description *= 2
        updated_short_url = storage.update(
            short_url=self.short_url,
            short_url_update=short_url_update,
        )
        self.assertNotEqual(
            source_description,
            updated_short_url.description,
        )
        self.assertEqual(
            short_url_update,
            ShortUrlUpdate(**updated_short_url.model_dump()),
        )

    def test_update_partial(self) -> None:
        short_url_update = ShortUrlUpdatePartial(
            description=self.short_url.description * 2
        )
        source_description = self.short_url.description
        updated_short_url = storage.update_partial(self.short_url, short_url_update)
        self.assertNotEqual(source_description, updated_short_url.description)

        self.assertEqual(short_url_update.description, updated_short_url.description)
