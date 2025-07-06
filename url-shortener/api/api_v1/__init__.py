from fastapi import APIRouter
from api.api_v1.short_urls.endpoints import router as short_url_router
from api.api_v1.short_urls.redirect_views import router as redirect_router

router = APIRouter(prefix="/v1")
router.include_router(router=short_url_router)
router.include_router(router=redirect_router)
