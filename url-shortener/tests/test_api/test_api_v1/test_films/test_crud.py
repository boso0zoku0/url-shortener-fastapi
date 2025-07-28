import string
from random import choices
from typing import ClassVar
from unittest import TestCase
from schemas.film import Films, FilmsCreate, FilmsUpdate, FilmsUpdatePartial
from api.api_v1.films.crud import storage


def create_film() -> Films:
    add_film = FilmsCreate(
        name="xxx",
        target_url="https://films.com",
        description="".join(
            choices(string.ascii_uppercase + string.ascii_lowercase, k=8)
        ),
        year_release=1999,
    )
    return add_film


class FilmsTestCase(TestCase):
    def setUp(self) -> None:
        self.film = create_film()

    def tearDown(self) -> None:
        storage.delete_films(self.film)

    def test_update_film(self) -> None:
        update_film = FilmsUpdate(**self.film.description * 2)
        source_description = update_film.description
        call_update_method = storage.update_film(source_description, update_film)

        self.assertNotEqual(source_description, call_update_method.description)

        self.assertEqual(update_film, call_update_method.description)

    def test_update_film_partial(self) -> None:
        film_update = FilmsUpdatePartial(**self.film.description * 2)
        source_description = film_update.description
        call_update_method = storage.update_film_partial(
            source_description, film_update
        )
        self.assertNotEqual(source_description, call_update_method.description)

        self.assertEqual(film_update, call_update_method.description)


class FilmsStorageGetTestCase(TestCase):
    FILMS_COUNT = 3
    films: ClassVar[list[Films]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.film = [create_film() for _ in range(cls.FILMS_COUNT)]

    def tearDownClass(cls) -> None:
        for film in cls.films:
            storage.delete_films(film)

    def test_get_list(self) -> None:
        storage_get = storage.get_films()
        storage_class_get = self.films
        expected_slugs = {su.slug for su in storage_get}
        slugs = {su.slug for su in self.films}
        result = expected_slugs - slugs
        expected_result = set()
        self.assertEqual(expected_result, result)

    def test_get_by_slug(self) -> None:
        for film in self.films:
            with self.subTest(slug=film.slug, msg=f"Validate slug {film.slug}"):
                db_get = storage.get_by_slug(film.slug)

                self.assertEqual(film.slug, db_get.slug)
