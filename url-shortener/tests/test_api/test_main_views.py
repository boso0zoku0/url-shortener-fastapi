import pytest
from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app)


def test_main_views():
    name = "Bob"
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert "message" in response_data
    assert response_data["message"] == f"Hello {name}", response_data


@pytest.mark.parametrize("name", ["John", "!@#$%&", "John Snow", ""])
def test_main_custom_views(name: str):
    query = {"name": name}
    response = client.get("/", params=query)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert "message" in response_data
    assert response_data["message"] == f"Hello {name}", response_data
