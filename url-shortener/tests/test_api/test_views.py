import pytest
from fastapi.testclient import TestClient
from fastapi import status

from tests.test_api.conftest import client


def test_main_views(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    expected_message = "Hello World"
    assert response_data["message"] == expected_message


@pytest.mark.parametrize("name", ["John", "!@#$%&", "John Snow", ""])
def test_main_custom_views(name: str, client: TestClient) -> None:
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert "message" in response_data
    assert response_data["message"] == f"Hello {name}", response_data
