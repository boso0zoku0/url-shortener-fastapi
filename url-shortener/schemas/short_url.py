from typing import Annotated

from annotated_types import Len, MaxLen
from fastapi import Form
from pydantic import BaseModel, AnyHttpUrl

ShortAnnotated_10_symbol = Annotated[str, Len(min_length=3, max_length=20)]
ShortAnnotated_30_symbol = Annotated[str, MaxLen(30)]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: ShortAnnotated_30_symbol = ""


class ShortUrlCreate(ShortUrlBase):
    slug: ShortAnnotated_10_symbol


class ShortUrl(BaseModel):
    target_url: AnyHttpUrl
    description: ShortAnnotated_30_symbol = ""
    slug: str
    visits: int = 42


class ShortUrlRead(BaseModel):
    target_url: AnyHttpUrl
    description: ShortAnnotated_30_symbol = ""
    slug: str


class ShortUrlUpdate(BaseModel):
    target_url: AnyHttpUrl
    description: ShortAnnotated_30_symbol


class ShortUrlUpdatePartial(BaseModel):
    target_url: AnyHttpUrl | None = None
    description: ShortAnnotated_30_symbol | None = None
