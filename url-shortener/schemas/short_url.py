from typing import Annotated

from annotated_types import Len, MaxLen
from fastapi import Form
from pydantic import BaseModel, AnyHttpUrl

ShortAnnotated_10_symbol = Annotated[str, Len(min_length=3, max_length=10)]
ShortAnnotated_30_symbol = Annotated[str, MaxLen(30)]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: ShortAnnotated_30_symbol = ""


class ShortUrl(ShortUrlBase):
    slug: str
    visits: int = 42


class ShortUrlCreate(ShortUrlBase):
    slug: ShortAnnotated_10_symbol


class ShortUrlRead(ShortUrlBase):
    slug: str


class ShortUrlUpdate(ShortUrlBase):
    description: ShortAnnotated_30_symbol


class ShortUrlUpdatePartial(ShortUrlBase):
    target_url: AnyHttpUrl | None = None
    description: ShortAnnotated_30_symbol | None = None
    slug: ShortAnnotated_10_symbol | None = None
