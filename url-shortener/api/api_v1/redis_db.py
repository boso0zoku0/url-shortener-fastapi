import secrets
from abc import ABC, abstractmethod
from tokenize import generate_tokens

from core import config
from redis import Redis

redis_tokens = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    decode_responses=True,
)


class AbstractTokenHelper(ABC):

    @abstractmethod
    def token_exists(self, token) -> bool:
        pass

    @abstractmethod
    def add_token(self, token) -> None:
        pass

    @classmethod
    def generate_token(cls):
        return secrets.token_urlsafe(16)

    def generate_and_save_token(self):
        generate = self.generate_token()
        self.add_token(generate)


class RedisHelper(AbstractTokenHelper):
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

    def generate_token(self):
        random_token = secrets.token_urlsafe(16)

    def generate_and_save_token(self, token: str):
        save_random_token = self.generate_token()
        self.add_token(save_random_token)


redis = RedisHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set=config.REDIS_TOKENS_SET_NAME,
)
