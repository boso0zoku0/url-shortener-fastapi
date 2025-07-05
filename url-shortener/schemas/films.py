from pydantic import BaseModel


class FilmsBase(BaseModel):
    name: str
    description: str
    year_release: int


class Films(FilmsBase):
    id: int
