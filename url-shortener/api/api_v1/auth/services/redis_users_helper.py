from abc import abstractmethod

from .users_helper import AbstractUserHelper
from redis import Redis
from core import config


class RedisUsersHelper(AbstractUserHelper):
    def __init__(self, host: str, port: int, db: int) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_user_password(self, username: str) -> str | None:
        return self.redis.hget(config.REDIS_USERS_NAME, username)

    #
    # @classmethod
    # def check_passwords_match(cls, password_1, password_2) -> bool:
    #     return password_1 == password_2
    #
    # def validate_user_password(self, username, password) -> bool:
    #     password_db = self.get_user_password(username=username)
    #     if password_db is None:
    #         return False
    #     return self.check_passwords_match(password_1=password_db, password_2=password)


db_redis_users = RedisUsersHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USERS,
)
