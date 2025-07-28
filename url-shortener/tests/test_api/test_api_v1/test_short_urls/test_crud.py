import string
from random import choices
from typing import ClassVar, List
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


def create_short_url() -> ShortUrl:
    short_url = ShortUrlCreate(
        target_url="https://example.com",
        description="A short url",
        slug="".join(choices(string.ascii_letters, k=8)),
    )

    return storage.create(short_url)


class ShortUrlUpdateTestCase(TestCase):

    def setUp(self) -> None:
        self.short_url = create_short_url()

    def tearDown(self) -> None:
        storage.delete(self.short_url)

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


class ShortUrlStorageGetTestCase(TestCase):
    SHORT_URL_COUNT = 3
    short_urls: ClassVar[List[ShortUrl]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.short_urls = [create_short_url() for _ in range(cls.SHORT_URL_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for short_url in cls.short_urls:
            storage.delete(short_url)

    def test_get_list(self) -> None:
        short_urls = storage.get()
        expected_slugs = {su.slug for su in self.short_urls}
        slugs = {su.slug for su in short_urls}
        expected_diff = set()
        diff = expected_diff - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for short_url in self.short_urls:
            with self.subTest(
                slug=short_url.slug, msg=f"Validate can get slug {short_url.slug}"
            ):

                db_short_url = storage.get_by_slug(short_url.slug)
                self.assertEqual(short_url.slug, db_short_url.slug)
