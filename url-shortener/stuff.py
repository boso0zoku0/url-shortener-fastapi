from pydantic import BaseModel
from redis import Redis

from core import config
import os

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


class User(BaseModel):
    name: str
    age: int


data = User(name="zoku", age=22)
print(data.name)


data_dict = User(name="wduzoku", age=21313213213).model_dump()
print(data_dict["wduzoku"])

print(
    User(
        name="wduzoku",
        age=21313213213,
    ).model_dump(mode="json")
)


# @pytest.fixture(scope="function")
# def x(request):
#     return request.param * 3
#
# @pytest.fixture(scope="function")
# def y(request):
#     return request.param * 2
#
# @pytest.mark.parametrize(
#     "x, y",
#     [("a", "b"), ("c", "d")],
#     indirect=True
# )
# def test_indirect(x, y):
#     assert x = 'aaa'
#
# if __name__ == "__main__":
#     main()
