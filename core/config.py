from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE: Optional[str] = "电影列表接口"

    DESC: Optional[str] = """
    - 电影列表项目，基于Hello Flask 一书中的 实战项目
    - 实现： FastAPI ....
    """

    # 邮件发送相关
    MAIL_PASSWORD: str

    # JWT
    # token相关
    ALGORITHM: str = "HS256"  # 加密算法
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # token的时效 3 天 = 60 * 24 * 3

    ORIGINS: List[str] = [
        "http://localhost:3000"
        "http://127.0.0.1:3000"
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

    class Config:
        env_file = ".env"


settings = Settings()
