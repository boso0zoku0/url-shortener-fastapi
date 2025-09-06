from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.redis.connect.host,
    port=settings.redis.connect.port,
    db=settings.database.db_redis,
    decode_responses=True,
)


def main() -> None:
    print(redis.ping())
    redis.set("name", "zoku")
    redis.set("age", "22")
    redis.set("car", "bmw")
    print(redis.get("name"))
    print(redis.get("age"))
    redis.getdel("car")
    print(redis.get("car"))
    print(f"Name: {redis.get('name')}. Age: {redis.get('age')}")
    redis.delete("name")
    redis.delete("age")
    print(redis.get("name"))
    print(redis.get("age"))


if __name__ == "__main__":
    main()
