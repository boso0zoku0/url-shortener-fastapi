from unittest import TestCase

from api.api_v1.dependencies import UNSAFE_METHODS, prefetch_url
from api.api_v1.short_urls.crud import storage


class DependsTestCase(TestCase):

    def test_prefetch_url(self) -> None:
        slugs = {su.slug for su in storage.get()}
        for slug in slugs:
            prefetch_url(slug)
            self.assertTrue(slug)


class TestUnsafeMethods(TestCase):
    def test_unsafe_methods_doesnt_contain_safe_methods(self) -> None:
        safe_methods = {
            "GET",
            "OPTIONS",
            "HEAD",
        }
        assert not UNSAFE_METHODS & safe_methods

    def test_uppercase_unsafe_methods(self) -> None:
        assert all(method.isupper() for method in UNSAFE_METHODS)
