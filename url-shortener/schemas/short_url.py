from typing import Annotated

from annotated_types import Len, MaxLen, MinLen
from pydantic import AnyHttpUrl, BaseModel

ShortAnnotated_10_symbol = Annotated[str, Len(min_length=3, max_length=8)]
ShortAnnotated_30_symbol = Annotated[str, MaxLen(30), MinLen(0)]
DESCRIPTION_MAX_LENGTH = Annotated[str, MaxLen(300)]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DESCRIPTION_MAX_LENGTH = ""


class ShortUrlCreate(ShortUrlBase):
    slug: ShortAnnotated_10_symbol


class ShortUrl(BaseModel):
    target_url: AnyHttpUrl
    description: DESCRIPTION_MAX_LENGTH = ""
    slug: ShortAnnotated_10_symbol = ""
    visits: int = 42


class ShortUrlRead(BaseModel):
    target_url: AnyHttpUrl
    description: DESCRIPTION_MAX_LENGTH
    slug: str


class ShortUrlUpdate(BaseModel):
    target_url: AnyHttpUrl
    description: DESCRIPTION_MAX_LENGTH


class ShortUrlUpdatePartial(BaseModel):
    target_url: AnyHttpUrl | None = None
    description: DESCRIPTION_MAX_LENGTH | None = None
