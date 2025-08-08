import string
from random import choices

from fastapi.testclient import TestClient
from fastapi import status
from tests.test_api.conftest import short_url
from main import app
from schemas.short_url import ShortUrlCreate, ShortUrl


def test_create_short_url(client: TestClient) -> None:
    url = app.url_path_for("create_short_url")
    data = ShortUrlCreate(
        target_url="https://example.com",
        description="A short url",
        slug="".join(choices(string.ascii_letters, k=8))).model_dump(mode="json")
    response = client.post(url=url, json=data)
    response_data = response.json()
    received_data = {
        "target_url": data["target_url"],
        "description": data["description"],
        "slug": data["slug"],
    }
    assert data == received_data, f"Response JSON: {response.json()}"


def test_short_url_already_exists(auth_client: TestClient, short_url: ShortUrl) -> None:
    data = ShortUrlCreate(**short_url.model_dump())
    json = data.model_dump(mode="json")
    url = app.url_path_for("create_short_url")
    response = auth_client.post(url=url, json=json)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_json = response.json()
    expected_error = f"Short URL with slug = {short_url.slug} already exists"
    assert response_json["detail"] == expected_error
