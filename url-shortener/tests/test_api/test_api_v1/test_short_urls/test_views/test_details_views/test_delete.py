"""
функция создание шорт урла по в параметрах слаг который пркоинуть дальше

ффикстура которая возвраащет эту функцию


"""

import sys
from typing import Generator
import logging
import pytest
from _pytest.fixtures import SubRequest
from fastapi import status
from starlette.testclient import TestClient

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate
from main import app

pytestmark = pytest.mark.apitest


def create_short_url(slug: str) -> ShortUrl:
    short_url = ShortUrlCreate(
        target_url="https://example.com",
        description="A short url",
        slug=slug,
    )
    return storage.create(short_url)


@pytest.fixture(
    params=[
        pytest.param("abc", id="min slug"),
        pytest.param("qweas", id="max slug"),
    ]
)
def short_url(request: SubRequest) -> ShortUrl:
    return create_short_url(request.param)


def test_short_url_delete(auth_client: TestClient, short_url: ShortUrl) -> None:
    url = app.url_path_for("delete_slug", slug=short_url.slug)
    response = auth_client.delete(url=url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(short_url.slug)


def test_disabling_capturing(capsys):
    print("this output is captured")
    with capsys.disabled():
        print("output not captured, going directly to sys.stdout")
    print("this output is also captured")


# def test_output_capture(capfd):
#     print("Это stdout")
#     print("Это stderr", file=sys.stderr)
#     out, err = capfd.readouterr()
#     assert "stdout" in out
#     assert "stderr" in err
