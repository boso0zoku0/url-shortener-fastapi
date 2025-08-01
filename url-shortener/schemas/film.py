from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, AnyHttpUrl

ShortAnnotated_description = Annotated[str, MaxLen(50)]
ShortAnnotated_slug = Annotated[str, MaxLen(15)]


class FilmsBase(BaseModel):
    name: str
    target_url: AnyHttpUrl
    description: ShortAnnotated_description | None = ""
    year_release: int


class FilmsCreate(FilmsBase):
    pass
    slug: ShortAnnotated_slug


class Films(FilmsBase):
    notes: str = ""
    slug: ShortAnnotated_slug


class FilmsRead(FilmsCreate):
    pass


class FilmsUpdate(BaseModel):
    name: str
    target_url: AnyHttpUrl
    description: ShortAnnotated_description | None = ""
    year_release: int


class FilmsUpdatePartial(BaseModel):
    name: str | None = None
    target_url: AnyHttpUrl | None = None
    description: ShortAnnotated_description | None = None
    year_release: int | None = None
