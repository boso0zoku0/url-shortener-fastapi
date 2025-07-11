from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.api_v1.short_urls.crud import storage
from api.api_v1.films.crud import storage as film_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.init_storage_from_state()
    film_storage.init_storage_from_state()
    yield
