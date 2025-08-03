import logging
from fastapi import FastAPI
from api import router as api_router
from app_lifespan import lifespan
from core import config
from api.main_views import router as main_views_router
from api.redirect_views import router as redirect_views_router

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
app.include_router(router=redirect_views_router)
app.include_router(router=main_views_router)
