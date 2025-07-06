from fastapi import APIRouter
from .views import router as short_url_router
from .redirect_views import router as redirect_router

router = APIRouter(prefix="/v1")
router.include_router(router=short_url_router)
router.include_router(router=redirect_router)
