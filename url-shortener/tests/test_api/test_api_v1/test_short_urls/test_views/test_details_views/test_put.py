from collections.abc import Generator
from pydoc import describe

import pytest
from _pytest.fixtures import SubRequest
from fastapi.testclient import TestClient
from fastapi import status
from pydantic import AnyHttpUrl

from api.api_v1.short_urls.crud import storage
from tests.test_api.conftest import create_short_url_not_exists, create_short_url_random_slug
from main import app
from schemas.short_url import ShortUrlCreate, ShortUrl, DESCRIPTION_MAX_LENGTH


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
            pytest.param("", "a" * DESCRIPTION_MAX_LENGTH, id="no desc to max desc"),
        ],
        indirect=["short_url"]
    )
    
    def test_short_url_update_partial(self, new_description: str, auth_client: TestClient, short_url: ShortUrl):
        url = app.url_path_for("put_short_url", slug=short_url.slug)
        response = auth_client.patch(url, json={"description": new_description})
        new_desc_db = storage.get_by_slug(short_url.slug)
        assert new_description == new_desc_db.description
        assert response.status_code == status.HTTP_200_OK
        assert short_url.description != new_desc_db.description

# target_url
# desc
# slug


class TestShortUrlUpdate:
    
    @pytest.fixture()
    def short_url(self, request: SubRequest) -> Generator[ShortUrl]:
        desc, target_url = request.param
        short_url = create_short_url_random_slug(description=desc, target_url=target_url)
        yield short_url
        storage.delete(short_url)
        
    @pytest.mark.parametrize(
        "short_url, new_description, new_target_url",
        [
            pytest.param(
                ("old_desc", "https://www.qweasd.com/"),
                "new_desc",
                "https://www.example.com/",
                id="new desc and url"
            ),
            pytest.param(
                ("old desc", "https://www.dsadwqwdq.com/"),
                "new desc",
                "https://www.dwqdwqdwqdq.com/",
                id="new desc"
            ),
        ],
        indirect=["short_url"]
    )
    
    def test_put_update_short_url(self, auth_client: TestClient, short_url: ShortUrl, new_description: str, new_target_url: str | AnyHttpUrl):
        url = app.url_path_for("put_short_url", slug=short_url.slug)
        new_short_url = ShortUrlCreate(description=new_description, target_url=new_target_url)
        response = auth_client.put(url, json=new_short_url.model_dump(mode="json"))
        assert response.status_code == status.HTTP_200_OK
        assert short_url.description != new_description