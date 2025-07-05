from pydantic import BaseModel


class ShortUrl(BaseModel):
    target_url: str
    slug: str
