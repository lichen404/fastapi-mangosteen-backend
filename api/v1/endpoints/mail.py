import random
import string
from fastapi import APIRouter, Depends, Request
from fastapi.background import BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel, Field
from core import settings
from core.redis import get_redis
from slowapi import Limiter
from slowapi.util import get_remote_address

mail = APIRouter(tags=["发送邮件"])

limiter = Limiter(key_func=get_remote_address)

class EmailSchema(BaseModel):
    email: EmailStr = Field(examples=["2725546002@qq.com"])


conf = ConnectionConfig(
    MAIL_USERNAME="2725546002@qq.com",
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM="2725546002@qq.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.qq.com",
    MAIL_FROM_NAME="lichen",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))


@mail.post("/validation_codes", summary="发送验证码")
@limiter.limit("1/minute")
async def send_in_background(
        request: Request,
        background_tasks: BackgroundTasks,
        email: EmailSchema,
        redis=Depends(get_redis)
) -> JSONResponse:
    code = generate_verification_code()
    user_email = email.model_dump().get("email")
    redis.set(user_email, code, ex=300)
    message = MessageSchema(
        subject="山竹记账验证码",
        recipients=[user_email],
        body=f'你正在登录山竹记账，验证码是{code}，验证码五分钟内有效。',
        subtype=MessageType.plain)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})


