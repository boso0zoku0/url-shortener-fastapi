from .users_helper import AbstractUserHelper
from redis import Redis
from core import config


class RedisUsersHelper(AbstractUserHelper):
    def __init__(self, host: str, port: int, db: int, tokens_set: str) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)
        self.tokens_set = tokens_set

    def get_user_password(self, username: str) -> bool:
        return bool(self.redis.sismember(self.tokens_set, username))

    def check_passwords_match(self, password_1, password_2) -> bool:
        return password_1 == password_2

    def validate_user_password(self, username, password) -> bool:
        password_db = self.get_user_password(username=username)
        if password_db is None:
            return False
        self.check_passwords_match(password_1=password_db, password_2=password)
        return True


db_redis_users = RedisUsersHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USERS,
    tokens_set=config.REDIS_TOKENS_SET_NAME,
)
