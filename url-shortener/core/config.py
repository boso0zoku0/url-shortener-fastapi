import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short_urls.json"


LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# вход по httpbearer
API_TOKENS: frozenset[str] = frozenset(
    {"eD83xIM7oJMn-WmuiDJPJQ", "HDk4YMx_Lu54ETlueqxTdw"}
)

# вход по httpbasic
DB_USERS: dict[str, str] = {"user1": "password1"}


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    datefmt: str = "%Y-%m-%d %H:%M:%S"


class RedisConnect(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisConfig(BaseModel):
    connect: RedisConnect = RedisConnect()


class DataBase(BaseModel):
    db_redis: int = 0
    db_redis_tokens: int = 1
    db_redis_users: int = 2
    db_redis_short_url: int = 3


class RedisNames(BaseModel):
    redis_tokens_name: str = "tokens"
    redis_users_name: str = "users"
    redis_short_url_hash_name: str = "short_urls"


class Settings(BaseSettings):
    logging_config: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()
    database: DataBase = DataBase()
    redis_names: RedisNames = RedisNames()


settings = Settings()
