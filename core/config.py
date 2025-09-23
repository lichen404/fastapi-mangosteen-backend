from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TITLE: Optional[str] = "山竹记账接口"

    DESC: Optional[str] = """
    - 山竹记账接口，基于饥人谷山竹记账项目
    - 实现： FastAPI ....
    """

    # 邮件发送相关
    MAIL_PASSWORD: str = ""

    # JWT
    # token相关
    ALGORITHM: str = "HS256"  # 加密算法
    SECRET_KEY: str = ""

    ORIGINS: List[str] = [
        "http://localhost:3000"
        "http://127.0.0.1:3000"
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://mangosteen.lichen404.top",
        "*"
    ]

    class Config:
        env_file = ".env"


settings = Settings()
