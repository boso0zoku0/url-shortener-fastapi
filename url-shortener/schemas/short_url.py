from typing import Annotated

from annotated_types import Len, MaxLen
from fastapi import Form
from pydantic import BaseModel, AnyHttpUrl


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: Annotated[str, MaxLen(30)] | None = ""


class ShortUrl(ShortUrlBase):
    # id: int
    slug: str


class ShortUrlCreate(ShortUrlBase):
    slug: Annotated[str, Len(min_length=3, max_length=10)]


class ShortUrlUpdate(ShortUrlBase):
    description: Annotated[str, MaxLen(30)]
