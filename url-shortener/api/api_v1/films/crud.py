from schemas.film import *
from pydantic import BaseModel
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


class FilmsBaseError(Exception):
    pass


class FilmsAlreadyExists(FilmsBaseError):
    pass


class FilmsStorage(BaseModel):
    slug_by_films: dict[str, FilmsRead] = {}

    def save_films(self, film: FilmsRead):
        redis.hset(
            name=config.REDIS_FILMS_HASH_NAME,
            key=film.slug,
            value=film.model_dump_json(),
        )

    def get_films(self):
        return [
            FilmsRead.model_validate_json(value)
            for value in redis.hvals(name=config.REDIS_FILMS_HASH_NAME)
        ]

    def get_by_slug(self, slug: str) -> FilmsRead | None:
        get_data = redis.hget(name=config.REDIS_FILMS_HASH_NAME, key=slug)
        if get_data:
            return FilmsRead.model_validate_json(get_data)
        return None

    def create_film(self, create_films: FilmsCreate) -> FilmsRead:
        add_film = FilmsRead(**create_films.model_dump())
        self.save_films(add_film)
        log.info("Created film: %s", add_film)
        return add_film

    def exists(self, slug: str) -> bool:
        return redis.hexists(name=config.REDIS_FILMS_HASH_NAME, key=slug)

    def create_or_raise_if_exists(self, film: FilmsCreate) -> FilmsRead:
        if not self.exists(film.slug):
            return storage.create_film(film)
        raise FilmsAlreadyExists(film.slug)

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(config.REDIS_FILMS_HASH_NAME, slug)
        log.info("Deleted film: %s", slug)

    def delete(self, film_url: FilmsRead) -> None:
        return self.delete_by_slug(slug=film_url.slug)

    def update(self, film: FilmsRead, film_update: FilmsUpdate) -> FilmsRead:
        for k, v in film_update:
            setattr(film, k, v)
        self.save_films(film)
        log.info("Updated film to %s", film)
        return film

    def update_partial(
        self, film: FilmsRead, film_update_partial: FilmsUpdatePartial
    ) -> FilmsRead:
        for k, v in film_update_partial.model_dump(exclude_unset=True).items():
            setattr(film, k, v)
        self.save_films(film)
        log.info("Updated film to %s", film)
        return film


storage = FilmsStorage()
