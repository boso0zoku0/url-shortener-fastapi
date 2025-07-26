from schemas.film import FilmsCreate, Films, FilmsUpdate, FilmsUpdatePartial
from unittest import TestCase


class FilmsTestCase(TestCase):
    def test_film_can_be_created_from_create_scheme(self) -> None:
        film_in = FilmsCreate(
            name="Matrix",
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
            description=None,
            year_release=1999,
        )
        film = FilmsUpdatePartial(**film_in.model_dump())
        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)
