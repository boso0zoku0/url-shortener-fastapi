import sys
import os
import pytest


@pytest.mark.skipif(os.name != "nt", reason="run only on Windows")
def test_platform() -> None:
    assert os.name == "nt"
    assert sys.platform == "win32"


@pytest.mark.skipif(os.name == "nt", reason="run on everything except Windows")
def test_platform_if() -> None:
    assert os.name != "nt"
    assert sys.platform != "win32"
