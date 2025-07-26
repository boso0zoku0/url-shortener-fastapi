from schemas.film import FilmsCreate, Films, FilmsUpdate, FilmsUpdatePartial
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


class FilmsSubTestTestCase(TestCase):

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
