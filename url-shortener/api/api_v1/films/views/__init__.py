__all__ = ("router",)

from .details_router import router as details_router
from .list_router import router

router.include_router(router=details_router)
