from schemas.film import FilmsCreate, Films
from unittest import TestCase


class FilmsTestCase(TestCase):
    def test_film_can_be_created_from_create_schema(self) -> None:
        film_in = FilmsCreate(
            name="Matrix",
            description="Is film Matrix",
            year_release=2000,
            slug="matrix",
        )

        film = Films(**film_in.model_dump())

        self.assertEqual(film.name, film_in.name)
        self.assertEqual(film.description, film_in.description)
        self.assertEqual(film.year_release, film_in.year_release)
        self.assertEqual(film.slug, film_in.slug)
