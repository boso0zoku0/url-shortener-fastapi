from fastapi import APIRouter

from .short_urls.views import router as views_router

router = APIRouter(prefix="/v1")
router.include_router(router=views_router)
