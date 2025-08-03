from unittest import TestCase
from api.api_v1.auth.services.redis_tokens_helper import db_redis_tokens


class RedisTokensHelperTestCase(TestCase):

    def test_generate_and_save_token(self) -> None:
        new_token = db_redis_tokens.generate_and_save_token()
        result = db_redis_tokens.token_exists(new_token)
        self.assertTrue(result)
