from fastapi import APIRouter

from rest.short_urls.create_views import router as create_views_router
from rest.short_urls.list_views import router as list_views_router

router = APIRouter(prefix="/short-urls", tags=["Short URLs REST"])
router.include_router(list_views_router)
router.include_router(create_views_router)
