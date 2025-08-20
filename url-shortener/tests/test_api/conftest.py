import random
import string
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl

from api.api_v1.auth.services import db_redis_tokens
from api.api_v1.short_urls.crud import storage
from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate

print("hi")


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def auth_token() -> Generator[str]:
    token = db_redis_tokens.generate_and_save_token()
    yield token
    db_redis_tokens.delete_token(token)


@pytest.fixture(scope="module")
def auth_client(auth_token: str) -> Generator[TestClient]:
    headers = {"Authorization": f"Bearer {auth_token}"}
    with TestClient(app, headers=headers) as client:
        yield client


def create_short_url() -> ShortUrl:
    short_url_in = ShortUrlCreate(
        target_url="https://example.com",
        description="A short url",
        slug="qweabc",
    )
    return storage.create(short_url_in)


@pytest.fixture()
def short_url() -> Generator[ShortUrl]:
    short_url = create_short_url()
    yield short_url
    storage.delete(short_url)


def build_short_url_create(
    slug: str,
    target_url: str | AnyHttpUrl = "https://www.example.com/",
    description: str = "A short url",
) -> ShortUrlCreate:
    return ShortUrlCreate(
        target_url=target_url,
        description=description,
        slug=slug,
    )


def build_short_url_create_random_slug(
    description: str = "It's desc",
    target_url: str | AnyHttpUrl = "https://www.example.com/",
) -> ShortUrlCreate:
    return build_short_url_create(
        slug="".join(random.choices(string.ascii_letters, k=8)),
        description=description,
        target_url=target_url,
    )


def create_short_url_not_exists(
    slug: str,
    target_url: str | AnyHttpUrl = "https://www.example.com/",
    description: str = "It's desc",
) -> ShortUrlCreate:
    short_url = build_short_url_create(
        slug, description=description, target_url=target_url
    )
    return storage.create(short_url)


def create_short_url_random_slug(
    target_url: str | AnyHttpUrl = "https://www.example.com/",
    description: str = "It's desc",
) -> ShortUrlCreate:
    short_url = build_short_url_create_random_slug(
        description=description, target_url=target_url
    )
    return storage.create_or_raise_if_exists(short_url)
