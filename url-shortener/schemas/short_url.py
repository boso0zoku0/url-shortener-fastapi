from typing import Annotated

from annotated_types import Len
from fastapi import Form
from pydantic import BaseModel, AnyHttpUrl


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    slug: str


class ShortUrl(ShortUrlBase):
    # id: int
    pass


class ShortUrlCreate(ShortUrlBase):
    slug: Annotated[str, Len(min_length=3, max_length=10)]
