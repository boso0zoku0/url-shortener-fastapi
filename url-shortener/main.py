from fastapi import FastAPI, status, HTTPException
from schemas.films import *
from api import router as api_router
import logging
from core import config
from app_lifespan import lifespan

log = logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
