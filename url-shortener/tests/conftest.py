from os import getenv

import pytest

if getenv("TESTING") != "1":
    raise pytest.exit("Environment variable TESTING must be 1")
