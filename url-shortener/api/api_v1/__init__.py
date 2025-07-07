from fastapi import APIRouter
from .short_urls.views import router as views_router
from .films.views import router as views_films_router

router = APIRouter(prefix="/v1")
router.include_router(router=views_router)
router.include_router(router=views_films_router)
