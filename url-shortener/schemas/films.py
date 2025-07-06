from pydantic import BaseModel
from typing import Annotated
from annotated_types import Len


class FilmsBase(BaseModel):
    name: str
    description: str
    year_release: int
    slug: str


class FilmsGet(FilmsBase):
    pass


class FilmsCreate(FilmsGet):
    slug: Annotated[str, Len(min_length=3, max_length=10)]
