from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlUpdate
from unittest import TestCase


class ShortUrlTestCase(TestCase):

    def test_short_url_can_be_created_from_create_schema(self) -> None:
        short_url_in = ShortUrlCreate(
            target_url="https://example.com",
            description="A short url example",
            slug="example",
        )

        short_url = ShortUrl(**short_url_in.model_dump())

        self.assertEqual(short_url_in.target_url, short_url.target_url)
        self.assertEqual(short_url_in.description, short_url.description)

    def test_short_url_can_be_created_from_update_schema(self) -> None:
        short_url_in = ShortUrlUpdate(
            target_url="https://example.com",
            description="A short url example",
        )

        short_url = ShortUrl(**short_url_in.model_dump())

        self.assertEqual(short_url_in.target_url, short_url.target_url)
        self.assertEqual(short_url_in.description, short_url.description)
