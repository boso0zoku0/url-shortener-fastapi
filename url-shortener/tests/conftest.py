from os import getenv

import pytest


@pytest.fixture(scope="session", autouse=True)
def checking_env():
    if getenv("TESTING") != "1":
        pytest.exit("This test must be run in test mode")
