import string
from random import choices
from unittest import TestCase
from schemas.film import Films, FilmsCreate, FilmsUpdate, FilmsUpdatePartial
from api.api_v1.films.crud import storage


class FilmsTestCase(TestCase):
    def setUp(self) -> None:
        self.film = self.create_film()

    def tearDown(self) -> None:
        storage.delete_films(self.film)

    def create_film(self) -> Films:
        add_film = FilmsCreate(
            name="xxx",
            target_url="https://films.com",
            description="".join(
                choices(string.ascii_uppercase + string.ascii_lowercase, k=8)
            ),
            year_release=1999,
        )
        return add_film

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
