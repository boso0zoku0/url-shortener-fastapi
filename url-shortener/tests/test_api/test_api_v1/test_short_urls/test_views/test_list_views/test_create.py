import logging
import random
import string

# from random import choices
from typing import Any

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate
from tests.test_api.conftest import (
    build_short_url_create_random_slug,
    short_url,
    build_short_url_create,
)

pytestmark = pytest.mark.apitest


def test_create_short_url(
    caplog: pytest.LogCaptureFixture, auth_client: TestClient
) -> None:
    caplog.set_level(logging.INFO)
    url = app.url_path_for("create_short_url")
    short_url = ShortUrlCreate(
        target_url="https://example.com",
        description="A short url",
        slug="".join(random.choices(string.ascii_letters, k=8)),
    )
    data: dict[str, str] = short_url.model_dump(mode="json")
    response = auth_client.post(url=url, json=data)
    response_data = response.json()
    received_data = {
        "target_url": data["target_url"],
        "description": data["description"],
        "slug": data["slug"],
    }
    assert response_data == received_data, f"Response JSON: {response.json()}"
    assert "Created short url" in caplog.text
    assert response_data["slug"] in caplog.text
    assert short_url.slug in caplog.text


def test_short_url_already_exists(auth_client: TestClient, short_url: ShortUrl) -> None:
    data = ShortUrlCreate(**short_url.model_dump())
    json = data.model_dump(mode="json")
    url = app.url_path_for("create_short_url")
    response = auth_client.post(url=url, json=json)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_json = response.json()
    expected_error = f"Short URL with slug = {short_url.slug} already exists"
    assert response_json["detail"] == expected_error


class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="too-short"),
            pytest.param(("foo-bar-spam-eggs", "string_too_long"), id="too-long"),
        ],
    )
    def short_url_values(self, request: SubRequest) -> tuple[dict[str, Any], str]:
        build = build_short_url_create_random_slug()
        build_json = build.model_dump(mode="json")
        slug, error = request.param
        build_json["slug"] = slug
        return build_json, error

    def test_invalid_slug(
        self, short_url_values: tuple[dict[str, Any], str], auth_client: TestClient
    ) -> None:
        url = app.url_path_for("create_short_url")
        create, error = short_url_values
        response = auth_client.post(url=url, json=create)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == error, error_detail
