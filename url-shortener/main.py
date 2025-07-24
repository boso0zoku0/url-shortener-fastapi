import logging

from fastapi import FastAPI

from api import router as api_router
from app_lifespan import lifespan
from core import config

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
