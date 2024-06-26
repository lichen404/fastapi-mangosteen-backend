"""
create app
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from slowapi.middleware import SlowAPIMiddleware
from settings import TORTOISE_ORM
from  .v1.endpoints.mail import limiter
from .v1 import v1
from core import settings



app = FastAPI(title=settings.TITLE, description=settings.DESC)

# 添加 SlowAPIMiddleware 中间件
app.add_middleware(SlowAPIMiddleware)

# 将默认的速率限制处理器添加到应用中
app.state.limiter = limiter

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
