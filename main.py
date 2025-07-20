from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
import logging
from core import config
from app_lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(router=api_router)

log = logging.basicConfig(format=config.LOG_FORMAT, level=config.LOG_LEVEL)


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
