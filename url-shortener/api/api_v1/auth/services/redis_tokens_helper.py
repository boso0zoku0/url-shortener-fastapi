import secrets

from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractTokenHelper
from core import config


class RedisTokensHelper(AbstractTokenHelper):
    def __init__(self, host: str, port: int, db: int, tokens_set: str) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set = tokens_set

    def token_exists(self, token) -> bool:
        return bool(self.redis.sismember(self.tokens_set, token))

    def add_token(self, token) -> None:
        self.redis.sadd(self.tokens_set, token)

    def get_all_tokens(self) -> list[str]:
        return list(self.redis.smembers(self.tokens_set))

    def generate_token(self):
        secrets.token_urlsafe(16)

    def generate_and_save_token(self, token: str):
        save_random_token = self.generate_token()
        self.add_token(save_random_token)


db_redis_tokens = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set=config.REDIS_TOKENS_NAME,
)
