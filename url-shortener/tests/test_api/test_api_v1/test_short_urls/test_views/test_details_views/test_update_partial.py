from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from starlette import status
from starlette.testclient import TestClient

from main import app
from schemas.short_url import ShortUrl
from storage.short_urls.crud import storage
from tests.test_api.conftest import create_short_url_random_slug

pytestmark = pytest.mark.apitest


class TestShortUrlUpdatePartial:

    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        short_url = create_short_url_random_slug(description=request.param)
        yield short_url
        storage.delete(short_url)

    @pytest.mark.parametrize(
        "short_url, new_description",
        [
            pytest.param("sdafasfawqesda", "", id="max desc to min desc"),
            pytest.param("", "a" * 40, id="no desc to max desc"),
        ],
        indirect=["short_url"],
    )
    def test_short_url_update_partial(
        self, new_description: str, auth_client: TestClient, short_url: ShortUrl
    ) -> None:
        url = app.url_path_for("put_short_url", slug=short_url.slug)
        response = auth_client.patch(url, json={"description": new_description})
        new_desc_db = storage.get_by_slug(short_url.slug)
        if new_desc_db:
            assert new_description == new_desc_db.description
            assert response.status_code == status.HTTP_200_OK
            assert short_url.description != new_desc_db.description
