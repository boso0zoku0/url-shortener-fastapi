from fastapi import APIRouter

from .films.views import router as views_films_router
from .short_urls.views import router as views_router

router = APIRouter(prefix="/v1")
router.include_router(router=views_router)
router.include_router(router=views_films_router)
