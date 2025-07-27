from unittest import TestCase

from os import getenv

if getenv("TESTING") != "1":
    raise EnvironmentError("Environment variable TESTING must be 1")


def total(x: int, y: int) -> int:
    return x + y


class TotalTestCase(TestCase):

    def test_total(self) -> None:
        x = 2
        y = 3
        res = total(x, y)
        expected_res = x + y
        self.assertEqual(res, expected_res)
