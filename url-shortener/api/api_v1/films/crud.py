from schemas.films import *
from pydantic import BaseModel, ValidationError
from core.config import SHORT_URLS_STORAGE_FILEPATH
import logging

log = logging.getLogger(__name__)


class FilmsStorage(BaseModel):
    slug_by_films: dict[str, FilmsRead] = {}

    def save_state(self):
        log.info("Saved short urls storage state")
        SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=4))
        log.warning("Saved films storage state")

    @classmethod
    def from_state(cls):
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            log.warning("No short urls storage found")
            return FilmsStorage
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())

    def get_films(self) -> list[FilmsRead]:
        return list(self.slug_by_films.values())

    def get_by_slug(self, slug: str) -> FilmsRead | None:
        return self.slug_by_films.get(slug)

    def create_film(self, create_films: FilmsCreate) -> FilmsRead:
        new_film = FilmsRead(**create_films.model_dump())
        self.slug_by_films[new_film.slug] = new_film
        self.save_state()
        log.info("Created film %s", new_film)
        return new_film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_by_films.pop(slug, None)
        self.save_state()
        log.info("Deleted film %s", slug)

    def delete(self, film_url: FilmsRead) -> None:
        return self.delete_by_slug(slug=film_url.slug)

    def update(self, film: FilmsRead, film_update: FilmsUpdate) -> FilmsRead:
        for k, v in film_update:
            setattr(film, k, v)
        self.save_state()
        log.info("Updated film to %s", film)
        return film

    def update_partial(
        self, film: FilmsRead, film_update_partial: FilmsUpdatePartial
    ) -> FilmsRead:
        for k, v in film_update_partial.model_dump(exclude_unset=True).items():
            setattr(film, k, v)
        self.save_state()
        return film


try:
    storage = FilmsStorage.from_state()
except ValidationError:
    storage = FilmsStorage()
    storage.write_text_in_file()
