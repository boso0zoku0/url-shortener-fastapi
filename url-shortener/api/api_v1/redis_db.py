from core import config
from redis import Redis


redis_tokens = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    decode_responses=True,
)
