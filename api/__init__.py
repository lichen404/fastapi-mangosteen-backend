"""
create app
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from settings import TORTOISE_ORM

from .v1 import v1
from core import settings

app = FastAPI(title=settings.TITLE, description=settings.DESC)

app.include_router(v1, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    config=TORTOISE_ORM
)
