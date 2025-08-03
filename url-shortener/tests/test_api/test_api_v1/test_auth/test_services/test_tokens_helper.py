# import random
# import string
# from typing import ClassVar, List
# from unittest import TestCase
#
#
# class TokensHelperTestCase(TestCase):
#     tokens: List[str] = []
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         for _ in range(5):
#             cls.tokens.append("".join(random.choices(string.ascii_lowercase, k=5)))
#
#     @classmethod
#     def tearDownClass(cls) -> None:
#         for token in cls.tokens:
#             cls.tokens.remove(token)
#
#     def test_token_exists(self) -> bool:
#         tokens_db = self.tokens
#         for token in tokens_db:
#             self.assertEqual(tokens_db)
