import logging
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILEPATH = BASE_DIR / "short_urls.json"


LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# вход по httpbearer
API_TOKENS: frozenset[str] = frozenset(
    {"eD83xIM7oJMn-WmuiDJPJQ", "HDk4YMx_Lu54ETlueqxTdw"}
)

# вход по httpbasic
DB_USERS: dict[str, str] = {"user1": "password1"}

# вход через редис
REDIS_HOST = "localhost"
REDIS_PORT = int(getenv("REDIS_PORT", "6379"))


REDIS_DB = 0

REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_SHORT_URLS = 3

REDIS_TOKENS_NAME = "tokens"
REDIS_USERS_NAME = "users"
REDIS_SHORT_URLS_HASH_NAME = "short_urls"
