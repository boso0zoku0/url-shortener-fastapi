import pytest
from starlette import status
from starlette.testclient import TestClient

from main import app


@pytest.mark.xfail(
    reason="not implemented yet",
    raises=ValueError,
)
@pytest.mark.apitest
def test_transfer(auth_client: TestClient) -> None:
    url = app.url_path_for("transfer_short_url")
    response = auth_client.post(url=url)
    assert response.status_code == status.HTTP_200_OK
