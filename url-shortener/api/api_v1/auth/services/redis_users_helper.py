__all__ = ("db_redis_users",)

from typing import cast

from redis import Redis

from core import config

from .users_helper import AbstractUserHelper


class RedisUsersHelper(AbstractUserHelper):
    def __init__(self, host: str, port: int, db: int) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_user_password(self, username: str) -> str:
        return cast(str, self.redis.hget(config.REDIS_USERS_NAME, username))


db_redis_users = RedisUsersHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USERS,
)
