import logging

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from api.redirect_views import router as redirect_views_router
from app_lifespan import lifespan
from core.config import settings
from rest import router as rest_router

logging.basicConfig(
    format=settings.logging.log_format,
    level=settings.logging.log_level,
    datefmt=settings.logging.datefmt,
)
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
app.include_router(router=redirect_views_router)
app.include_router(router=rest_router)


if __name__ == "__main__":
    uvicorn.run(app=app)
