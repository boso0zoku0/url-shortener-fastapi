from fastapi import APIRouter

from .api_v1 import router as api_v1_router

# from .api_v1.films.endpoints import router as films_router

router = APIRouter(prefix="/api")
router.include_router(router=api_v1_router)
# router.include_router(router=films_router)
