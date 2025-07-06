from schemas.films import *
from pydantic import BaseModel


class FilmsStorage(BaseModel):
    slug_by_films: dict[str, FilmsGet] = {}

    def get_films(self) -> list[FilmsGet]:
        return list(self.slug_by_films.values())

    def get_by_slug_film(self, slug: str) -> FilmsGet | None:
        return self.slug_by_films.get(slug)

    def create_film(self, create_films: FilmsCreate) -> FilmsGet:
        new_film = FilmsGet(**create_films.model_dump())
        self.slug_by_films[new_film.slug] = new_film
        return new_film


storage = FilmsStorage()

storage.create_film(
    FilmsCreate(
        name="Криминальное чтиво",
        description="Нелинейная криминальная драма",
        year_release=1994,
        slug="Чтиво",
    )
)

storage.create_film(
    FilmsCreate(
        name="Интерстеллар",
        description="Космическая одиссея о спасении человечества",
        year_release=2014,
        slug="Интер",
    )
)

storage.create_film(
    FilmsCreate(
        name="Матрица",
        description="Реальность иллюзия виртуального мира",
        year_release=1999,
        slug="МТЦ",
    )
)
