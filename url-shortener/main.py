from api import router as api_router
import logging
from core import config
from app_lifespan import lifespan
from fastapi import FastAPI
import typer

logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)
app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)
