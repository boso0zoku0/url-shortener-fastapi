__all__ = ("db_redis_users",)

from typing import cast

from redis import Redis

from core import config
from core.config import settings

from .users_helper import AbstractUserHelper


class RedisUsersHelper(AbstractUserHelper):
    def __init__(self, host: str, port: int, db: int) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_user_password(self, username: str) -> str:
        return cast(
            str, self.redis.hget(settings.redis.redis_names.redis_users_name, username)
        )


db_redis_users = RedisUsersHelper(
    host=settings.redis.connect.host,
    port=settings.redis.connect.port,
    db=settings.redis.database.db_redis_users,
)
