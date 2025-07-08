from schemas.films import *
from pydantic import BaseModel


class FilmsStorage(BaseModel):
    slug_by_films: dict[str, FilmsRead] = {}

    def get_films(self) -> list[FilmsRead]:
        return list(self.slug_by_films.values())

    def get_by_slug(self, slug: str) -> FilmsRead | None:
        return self.slug_by_films.get(slug)

    def create_film(self, create_films: FilmsCreate) -> FilmsRead:
        new_film = FilmsRead(**create_films.model_dump())
        self.slug_by_films[new_film.slug] = new_film
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_by_films.pop(slug, None)

    def delete(self, film_url: FilmsRead) -> None:
        return self.delete_by_slug(slug=film_url.slug)

    def update(self, film: FilmsRead, film_update: FilmsUpdate) -> FilmsRead:
        for k, v in film_update:
            setattr(film, k, v)
        return film

    def update_partial(
        self, film: FilmsRead, film_update_partial: FilmsUpdatePartial
    ) -> FilmsRead:
        for k, v in film_update_partial.model_dump(exclude_unset=True).items():
            setattr(film, k, v)
        return film


storage_films = FilmsStorage()

storage_films.create_film(
    FilmsCreate(
        name="Криминальное чтиво",
        description="Нелинейная криминальная драма",
        year_release=1994,
        slug="Чтиво",
    )
)

storage_films.create_film(
    FilmsCreate(
        name="Интерстеллар",
        description="Космическая одиссея о спасении человечества",
        year_release=2014,
        slug="Интер",
    )
)

storage_films.create_film(
    FilmsCreate(
        name="Матрица",
        description="Реальность иллюзия виртуального мира",
        year_release=1999,
        slug="МТЦ",
    )
)
