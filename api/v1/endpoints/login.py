from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from core.redis import get_redis
from models import User
from core import create_access_token

login = APIRouter(tags=["认证相关"])


class Token(BaseModel):
    jwt: str


class Form(BaseModel):
    email: str
    code: str


@login.post("/session", summary="登录")
async def user_login(form: Form, redis=Depends(get_redis)):
    if stored_code := redis.get(form.email):
        if form.code != stored_code.decode():
            raise HTTPException(status_code=400, detail="Invalid verification code")
        if user := await User.get_or_create(email=form.email):
            token = create_access_token({"user_id": user[0].pk})
            return Token(jwt=token)
    raise HTTPException(status_code=404, detail="Verification code not found")
