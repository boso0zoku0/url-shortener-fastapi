import string
import random
from collections.abc import Generator
from typing import ClassVar, Any, cast
from unittest import TestCase

import pytest

from schemas.film import Films, FilmsCreate, FilmsUpdate, FilmsUpdatePartial, FilmsRead
from api.api_v1.films.crud import storage, FilmsAlreadyExistsError


def creation_film() -> Films:
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


@pytest.fixture
def film() -> Generator[FilmsRead]:
    film = creation_film()
    yield film
    storage.delete(film)


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
        cls.films = [creation_film() for _ in range(cls.FILMS_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for film in cls.films:
            storage.delete(film)

    def test_get_list(self) -> None:
        storage_get = storage.get_films()
        storage_class_get = self.films
        expected_slugs = {su.slug for su in self.films}
        slugs = {su.slug for su in storage_get}

        diff = expected_slugs - slugs
        expected_diff = set()
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for film in self.films:
            with self.subTest(slug=film.slug, msg=f"Validate slug {film.slug}"):
                db_get = storage.get_by_slug(film.slug)

                self.assertEqual(film.slug, db_get.slug)


def test_create_or_raise_if_exist(film: FilmsRead) -> None:
    film_create = FilmsCreate(**film.model_dump())
    with pytest.raises(FilmsAlreadyExistsError, match=film_create.slug) as exc_info:
        storage.create_or_raise_if_exists(film_create)
    assert exc_info.value.args[0] == film_create.slug
