import string

from pydantic import ValidationError

from schemas.film import FilmsCreate, Films, FilmsUpdate, FilmsUpdatePartial, FilmsRead
from unittest import TestCase


class FilmsTestCase(TestCase):
    def test_film_can_be_created_from_create_scheme(self) -> None:
        film_in = FilmsCreate(
            name="Matrix",
            target_url="https://example.com",
            description="Is film Matrix",
            year_release=2000,
        )

        film = Films(**film_in.model_dump())

        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)

    def test_film_can_be_created_from_update_scheme(self) -> None:
        film_in = FilmsUpdate(
            name="Matrix",
            target_url="https://example.com",
            description="Is film Matrix",
            year_release=2000,
        )

        film = Films(**film_in.model_dump())

        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)

    def test_empty_movie_can_be_created_from_partial_update_scheme(self) -> None:
        film_in = FilmsUpdatePartial(
            name=None,
            target_url=None,
            description=None,
            year_release=None,
        )
        film = FilmsUpdatePartial(**film_in.model_dump())
        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)

    def test_partially_filled_film_can_be_created_from_the_partial_update_scheme(
        self,
    ) -> None:
        film_in = FilmsUpdatePartial(
            name="Matrix",
            target_url="https://example.com",
            description=None,
            year_release=1999,
        )
        film = FilmsUpdatePartial(**film_in.model_dump())
        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.target_url, film_in.target_url)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)


class FilmsComplicatedTestCase(TestCase):

    def test_films_create_accepts_different_urls(self) -> None:
        urls = [
            "https://example.com",
            "https://www.example.com",
            "https://example",
        ]

        for url in urls:
            with self.subTest(url=url, msg=f"added url: {url}"):
                film_in = FilmsCreate(
                    name="test_film",
                    target_url=url,
                    description="Is new film",
                    year_release=1999,
                )
                self.assertEqual(
                    url.rstrip("/"),
                    film_in.model_dump(mode="json")["target_url"].rstrip("/"),
                )

    def test_films_update_accepts_different_urls(self) -> None:
        names = ["Matrix", "maTriX", "Clan @Soprano", " dw цв"]

        for name in names:
            with self.subTest(name=names, msg=f"new name: {name}"):
                film_in = FilmsUpdate(
                    name=name,
                    target_url="https://kinopoisk.com",
                    description="Is new film",
                    year_release=1999,
                )
                self.assertEqual(name, film_in.model_dump(mode="json")["name"])

    def test_films_slug_too_long(self) -> None:

        with self.assertRaises(ValidationError):
            FilmsCreate(
                name="test_film",
                target_url="https://example.com",
                description="This string contains more than thirty alphabetic characters.",
                year_release=1999,
            )

    def test_films_create_slug_long_film_with_regex(self) -> None:

        with self.assertRaisesRegex(
            ValidationError,
            expected_regex="String should have at most 50 characters",
        ) as exc_info:
            FilmsCreate(
                name="test_film",
                target_url="https://example.com",
                description="This string contains more than thirty alphabetic characters.",
                year_release=1999,
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_long"
        self.assertEqual(expected_type, error_details["type"])

    def test_films_error(self) -> None:
        data_film_read = FilmsRead(
            name="dwqwd",
            slug="dwqwd",
            target_url="https://example.com",
            description="Is new film",
            year_release=1999,
        )
        with self.assertRaisesRegex(
            AssertionError,
            expected_regex="'dwqwd' != 'dwqwdabcdefghijklmnopqrstuvwxyz'",
        ):
            data_films = Films(**data_film_read.model_dump())
            expected_film = data_films.name
            result = data_film_read.name + "".join(string.ascii_lowercase)
            self.assertEqual(expected_film, result)
