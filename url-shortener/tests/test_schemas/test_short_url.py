import pytest
from pydantic import ValidationError
from os import getenv
from schemas.short_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlUpdatePartial,
)
from unittest import TestCase


class ShortUrlTestCase(TestCase):

    def test_short_url_can_be_created_from_create_schema(self) -> None:
        short_url_in = ShortUrlCreate(
            slug="short",
            target_url="https://example.com",
            description="A short url example",
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

    def test_empty_short_url_can_be_created_from_partial_update_scheme(self) -> None:
        short_url_in = ShortUrlUpdatePartial(
            target_url=None,
            description=None,
        )
        short_url = ShortUrlUpdatePartial(**short_url_in.model_dump())
        self.assertEqual(short_url_in.target_url, short_url.target_url)
        self.assertEqual(short_url_in.description, short_url.description)

    def test_partially_filled_short_url_can_be_created_from_the_partial_update_scheme(
        self,
    ) -> None:
        short_url_in = ShortUrlUpdatePartial(
            target_url=None,
            description=None,
        )
        short_url = ShortUrlUpdatePartial(**short_url_in.model_dump())
        self.assertEqual(short_url_in.target_url, short_url.target_url)
        self.assertEqual(short_url_in.description, short_url.description)


class ShortUrlsSubTestTestCase(TestCase):

    def test_short_url_create_accepts_different_urls(self) -> None:
        urls = [
            "https://example.com",
            "http://example.com",
            # "rtmp://example.com",
            # "rtmps://example.com",
            "https://example",
        ]

        for url in urls:
            with self.subTest(url=url, msg="added short url"):

                short_url_in = ShortUrlCreate(
                    target_url=url, slug="qweabc", description="another short url"
                )

                self.assertEqual(
                    url.rstrip("/"),
                    short_url_in.model_dump(mode="json")["target_url"].rstrip("/"),
                )


# String should have at most 30 characters
class ShortUrlsComplicatedTestCase(TestCase):

    def test_short_url_create_too_long_description(self) -> None:
        with self.assertRaises(ValidationError) as exc_type:
            ShortUrlCreate(
                target_url="https://example.com",
                slug="abcqwe",
                description="This string contains more than thirty alphabetic characters.",
            )
            error_type = exc_type.exception.errors()[0]
            expected_erorr = "string_too_long"
            self.assertEqual(expected_erorr, error_type["type"])

    def test_short_url_too_long_description_regex(self) -> None:
        with self.assertRaisesRegex(
            ValidationError, expected_regex="String should have at most 30 characters"
        ) as exc_info:
            ShortUrlCreate(
                target_url="https://example.com",
                slug="abcqwe",
                description="This string contains more than thirty alphabetic characters.",
            )
        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_long"

        self.assertEqual(expected_type, error_details["type"])
