from collections.abc import Generator

import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import AnyHttpUrl

from api.api_v1.short_urls.crud import storage
from main import app
from schemas.short_url import ShortUrl, ShortUrlCreate
from tests.test_api.conftest import (
    create_short_url_random_slug,
)

pytestmark = pytest.mark.apitest


class TestShortUrlUpdate:

    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        desc, target_url = request.param
        short_url = create_short_url_random_slug(
            description=desc, target_url=target_url
        )
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description, new_target_url",
        [
            pytest.param(
                ("old_desc", "https://www.qweasd.com/"),
                "new_desc",
                "https://www.example.com/",
                id="new desc and url",
            ),
            pytest.param(
                ("old desc", "https://www.dsadwqwdq.com/"),
                "new desc",
                "https://www.dwqdwqdwqdq.com/",
                id="new desc",
            ),
        ],
        indirect=["short_url"],
    )
    def test_put_update_short_url(
        self,
        auth_client: TestClient,
        short_url: ShortUrl,
        new_description: str,
        new_target_url: str | AnyHttpUrl,
    ) -> None:
        url = app.url_path_for("put_short_url", slug=short_url.slug)
        new_short_url = ShortUrlCreate(
            slug="qweabc", description=new_description, target_url=new_target_url
        )
        response = auth_client.put(url, json=new_short_url.model_dump(mode="json"))
        assert response.status_code == status.HTTP_200_OK
        assert short_url.description != new_description
