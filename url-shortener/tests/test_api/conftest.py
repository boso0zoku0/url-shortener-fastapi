
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient

from api.api_v1.auth.services import db_redis_tokens
from api.api_v1.short_urls.crud import storage
from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate


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


