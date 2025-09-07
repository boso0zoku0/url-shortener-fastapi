import logging
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short_urls.json"

ERROR_DB = "Database already exists"

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
    log_level_name: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: str = LOG_FORMAT
    datefmt: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class RedisConnect(BaseModel):
    host: str = "localhost"
    port: int = 6379


class DataBase(BaseModel):
    db_redis: int = 0
    db_redis_tokens: int = 1
    db_redis_users: int = 2
    db_redis_short_url: int = 3

    @model_validator(mode="after")
    def dbs_validate_unique_numbers(self) -> Self:
        db_values = list(self.model_dump().values())
        if len(set(db_values)) != len(db_values):
            raise ValueError(ERROR_DB)
        return self


class RedisNames(BaseModel):
    redis_tokens_name: str = "tokens"
    redis_users_name: str = "users"
    redis_short_url_hash_name: str = "short_urls"


class RedisConfig(BaseModel):
    connect: RedisConnect = RedisConnect()
    database: DataBase = DataBase()
    redis_names: RedisNames = RedisNames()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        env_nested_delimiter="__",
        env_prefix="URL_SHORTENER__",
    )
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


settings = Settings()
print(settings.logging)
print(settings.redis.database)
