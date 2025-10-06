__all__ = ("db_redis_tokens",)

import secrets
from typing import Iterable, cast

from redis import Redis

from api.api_v1.auth.services.tokens_helper import AbstractTokenHelper
from core.config import settings


class RedisTokensHelper(AbstractTokenHelper):
    def __init__(self, host: str, port: int, db: int, tokens_set: str) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set = tokens_set

    def token_exists(self, token: str) -> bool:
        return bool(self.redis.sismember(self.tokens_set, token))

    def add_token(self, token: str) -> None:
        cast(str, self.redis.sadd(self.tokens_set, token))

    def get_all_tokens(self) -> list[str]:
        return list(cast(Iterable[str], self.redis.smembers(self.tokens_set)))

    def delete_token(self, token: str) -> None:
        self.redis.srem(self.tokens_set, token)

    def generate_token(self) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


db_redis_tokens = RedisTokensHelper(
    host=settings.redis.connect.host,
    port=settings.redis.connect.port,
    db=settings.redis.database.db_redis_tokens,
    tokens_set=settings.redis.redis_names.redis_tokens_name,
)
