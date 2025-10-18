from unittest import TestCase

from services.auth import db_redis_tokens


class RedisTokensHelperTestCase(TestCase):

    def test_generate_and_save_token(self) -> None:
        new_token = db_redis_tokens.generate_and_save_token()
        result = db_redis_tokens.token_exists(new_token)
        self.assertTrue(result)
