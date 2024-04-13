from fastapi import APIRouter, Depends, Form, HTTPException
from pydantic import BaseModel
from core.redis import get_redis
from models import User
from core import create_access_token


login = APIRouter(tags=["认证相关"])


class Token(BaseModel):
    access_token: str
    token_type: str


@login.post("/login", summary="登录")
async def user_login(email: str = Form(), code: str = Form(), redis=Depends(get_redis)):
    if stored_code := redis.get(email):
        if code != stored_code.decode():
            raise HTTPException(status_code=400, detail="Invalid verification code")
        if user := await User.get_or_create(email=email):
            token = create_access_token({"user_id": user[0].pk})
            return Token(access_token=token, token_type="bearer")
    raise HTTPException(status_code=404, detail="Verification code not found")
