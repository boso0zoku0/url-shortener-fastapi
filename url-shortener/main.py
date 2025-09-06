import logging

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_views_router
from api.redirect_views import router as redirect_views_router
from app_lifespan import lifespan
from core.config import settings

logging.basicConfig(
    format=settings.logging_config.log_format,
    level=settings.logging_config.log_level,
    datefmt=settings.logging_config.datefmt,
)
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
app.include_router(router=redirect_views_router)
app.include_router(router=main_views_router)


if __name__ == "__main__":
    uvicorn.run(app=app)