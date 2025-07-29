import string

# from random import choices
import random
from typing import ClassVar
from unittest import TestCase
from schemas.film import Films, FilmsCreate, FilmsUpdate, FilmsUpdatePartial, FilmsRead
from api.api_v1.films.crud import storage
from os import getenv


if getenv("TESTING") != "1":
    raise EnvironmentError("Environment variable TESTING must be 1")


def creation_film() -> FilmsRead:
    film_in = FilmsCreate(
        name="dwq",
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        description="A film",
        target_url="https://example.com",
        year_release=1999,
    )
    return storage.create_film(film_in)


class FilmsUpdateTestCase(TestCase):

    def setUp(self) -> None:
        self.film = creation_film()

    def tearDown(self) -> None:
        storage.delete(self.film)

    def test_update_film(self) -> None:
        film_update = FilmsUpdate(**self.film.model_dump())
        source_description = film_update.description
        film_update.description *= 2
        film_updated = storage.update(film=self.film, film_update=film_update)

        self.assertNotEqual(source_description, film_updated.description)

        self.assertEqual(film_update, FilmsUpdate(**film_updated.model_dump()))

    def test_update_film_partial(self) -> None:
        film_update = FilmsUpdatePartial(**self.film.model_dump())
        source_description = film_update.description
        film_update.description *= 2
        film_updated = storage.update_partial(self.film, film_update)
        self.assertNotEqual(source_description, film_updated.description)

        self.assertEqual(film_update, FilmsUpdatePartial(**film_update.model_dump()))


class FilmsStorageGetTestCase(TestCase):
    FILMS_COUNT = 3
    films: ClassVar[list[Films]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.film = [creation_film() for _ in range(cls.FILMS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for film in cls.films:
            storage.delete_films(film)

    def test_get_list(self) -> None:
        storage_get = storage.get_films()
        storage_class_get = self.films
        expected_slugs = {su.slug for su in self.film}
        slugs = {su.slug for su in storage_get}

        diff = expected_slugs - slugs
        expected_diff = set()
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for film in self.films:
            with self.subTest(slug=film.slug, msg=f"Validate slug {film.slug}"):
                db_get = storage.get_by_slug(film.slug)

                self.assertEqual(film.slug, db_get.slug)
