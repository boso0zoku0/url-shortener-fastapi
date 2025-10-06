import pytest

from schemas.user import User, UserPost


code_password = "rgewejwdscvvcvmnte"


@pytest.mark.skip(reason="not implemented yet")
def test_user_schema() -> None:
    user_in = User(name="qwe", password=code_password)
    user = UserPost(**user_in.model_dump(mode="json"))
    assert user_in.name == user.name
