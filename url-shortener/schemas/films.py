from pydantic import BaseModel
from typing import Annotated
from annotated_types import Len, MaxLen


ShortAnnotated_10_symbol = Annotated[str, MaxLen(50)]


class FilmsBase(BaseModel):
    name: str
    description: ShortAnnotated_10_symbol | None = ""
    year_release: int
    slug: str


class FilmsGet(FilmsBase):
    pass


class FilmsCreate(FilmsGet):
    slug: Annotated[str, Len(min_length=3, max_length=50)]


class FilmsUpdate(FilmsGet):
    description: ShortAnnotated_10_symbol


class FilmsUpdatePartial(FilmsGet):
    name: str | None = None
    description: ShortAnnotated_10_symbol | None = None
    year_release: int | None = None
    slug: str | None = None
