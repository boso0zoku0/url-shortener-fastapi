from unittest import TestCase


def total(x: int, y: int) -> int:
    return x + y


class TotalTestCase(TestCase):

    def test_total(self) -> None:
        x = 2
        y = 3
        res = total(x, y)
        expected_res = x + y
        self.assertEqual(res, expected_res)
