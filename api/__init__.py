"""
create app
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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


# 定制错误信息的异常处理器
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 429:  # 针对速率限制错误
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error":"请求太快，请稍后再试",
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": str(exc.detail)
        }
    )
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
