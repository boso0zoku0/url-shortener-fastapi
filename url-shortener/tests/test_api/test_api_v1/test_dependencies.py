from os import getenv
from unittest import TestCase

import pytest

from api.api_v1.dependencies import prefetch_url, prefetch_url_film, UNSAFE_METHODS
from api.api_v1.short_urls.crud import storage
from api.api_v1.films.crud import storage as storage_film


class DependsTestCase(TestCase):

    def test_prefetch_url(self) -> None:
        slugs = {su.slug for su in storage.get()}
        for slug in slugs:
            prefetch_url(slug)
            self.assertTrue(slug)

    def test_prefetch_url_film(self) -> None:
        slugs = {su.slug for su in storage_film.get_films()}
        for slug in slugs:
            prefetch_url_film(slug)


class TestUnsafeMethods(TestCase):
    def test_unsafe_methods_doesnt_contain_safe_methods(self) -> None:
        safe_methods = {
            "GET",
            "OPTIONS",
            "HEAD",
        }
        assert not UNSAFE_METHODS & safe_methods

    def test_uppercase_unsafe_metgods(self) -> None:
        assert all(method.isupper() for method in UNSAFE_METHODS)
