from schemas.films import *
from pydantic import BaseModel, ValidationError, model_validator
from core.config import SHORT_URLS_STORAGE_FILEPATH
import logging
from core import config
from redis import Redis

log = logging.getLogger(__name__)


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_FILMS,
    decode_responses=True,
)


class FilmsStorage(BaseModel):
    slug_by_films: dict[str, FilmsRead] = {}

    def save_state(self):
        # log.info("Saved short urls storage state")
        for _ in range(15000):
            SHORT_URLS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=4))
        log.warning("Saved films storage state")

    @classmethod
    def from_state(cls):
        if not SHORT_URLS_STORAGE_FILEPATH.exists():
            log.warning("No short urls storage found")
            return FilmsStorage
        return cls.model_validate_json(SHORT_URLS_STORAGE_FILEPATH.read_text())

    def init_storage_from_state(self):
        try:
            data = FilmsStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Rewritten storage file due to validation error")
            return
        self.slug_by_films.update(data.slug_by_films)
        log.warning("Recovered data from storage file.")

    def get_films(self) -> list[FilmsRead]:
        return list(self.slug_by_films.values())

    def get_by_slug(self, slug: str) -> FilmsRead | None:
        get_data = redis.hget(name=config.REDIS_FILMS_HASH_NAME, key=slug)
        if get_data:
            return FilmsRead.model_validate_json(get_data)

    def create_film(self, create_films: FilmsCreate) -> FilmsRead:
        add_film = FilmsRead(**create_films.model_dump())
        redis.hset(
            name=config.REDIS_FILMS_HASH_NAME,
            key=add_film.slug,
            value=add_film.model_dump_json(),
        )
        # self.save_state()
        log.info("Created film %s", add_film)
        return add_film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_by_films.pop(slug, None)
        # self.save_state()
        log.info("Deleted film %s", slug)

    def delete(self, film_url: FilmsRead) -> None:
        return self.delete_by_slug(slug=film_url.slug)

    def update(self, film: FilmsRead, film_update: FilmsUpdate) -> FilmsRead:
        for k, v in film_update:
            setattr(film, k, v)
            # self.save_state()
        log.info("Updated film to %s", film)
        return film

    def update_partial(
        self, film: FilmsRead, film_update_partial: FilmsUpdatePartial
    ) -> FilmsRead:
        for k, v in film_update_partial.model_dump(exclude_unset=True).items():
            setattr(film, k, v)
        log.info("Updated film to %s", film)
        # self.save_state()
        return film


storage = FilmsStorage()
