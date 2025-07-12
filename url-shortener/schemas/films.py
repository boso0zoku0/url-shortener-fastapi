from pydantic import BaseModel
from typing import Annotated
from annotated_types import Len, MaxLen


ShortAnnotated_description = Annotated[str, MaxLen(50)]
ShortAnnotated_slug = Annotated[str, MaxLen(15)]


class FilmsBase(BaseModel):
    name: str
    description: ShortAnnotated_description | None = ""
    year_release: int


class FilmsCreate(FilmsBase):
    slug: ShortAnnotated_slug


class Films(FilmsBase):
    notes: str
    slug: ShortAnnotated_slug


class FilmsRead(FilmsBase):
    slug: ShortAnnotated_slug


class FilmsUpdate(FilmsBase):
    description: ShortAnnotated_description


class FilmsUpdatePartial(FilmsBase):
    name: str | None = None
    description: ShortAnnotated_description | None = None
    year_release: int | None = None
