from pydantic import BaseModel
from typing import Annotated
from annotated_types import Len, MaxLen


class FilmsBase(BaseModel):
    name: str
    description: Annotated[str, MaxLen(50)] | None = ""
    year_release: int
    slug: str


class FilmsGet(FilmsBase):
    pass


class FilmsCreate(FilmsGet):
    slug: Annotated[str, Len(min_length=3, max_length=50)]


class FilmsUpdate(FilmsGet):
    description: Annotated[str, MaxLen(50)]
