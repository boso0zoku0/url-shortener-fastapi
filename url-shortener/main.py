from fastapi import FastAPI, status, HTTPException
from schemas.films import *
from api import router as api_router

app = FastAPI()
app.include_router(router=api_router)
