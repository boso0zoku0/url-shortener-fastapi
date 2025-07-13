from fastapi import APIRouter
from starlette import status

from api.api_v1.short_urls.crud import storage
from schemas.short_url import ShortUrl, ShortUrlCreate, ShortUrlRead
from fastapi import Depends
from api.api_v1.dependencies import save_storage_state, basic_auth_validation

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[Depends(basic_auth_validation), Depends(save_storage_state)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


@router.get("/read-urls", response_model=list[ShortUrl])
def read_short_urls_list() -> list[ShortUrlRead]:
    return storage.get()


@router.post("/", response_model=ShortUrlRead, status_code=status.HTTP_201_CREATED)
def create_short_url(short_url: ShortUrlCreate):
    return storage.create(short_url)


@router.get("/search", response_model=ShortUrlRead)
def search_url(slug: str):
    return storage.get_by_slug(slug=slug)
