from redis import Redis

from core import config

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
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
