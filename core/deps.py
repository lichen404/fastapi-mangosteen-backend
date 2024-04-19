from fastapi import Depends, HTTPException, Header, Security
from fastapi import status
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError
from .config import settings
from models import User

token_key = APIKeyHeader(name="Authorization")


async def get_auth_header(auth_key: str = Security(token_key)):
    if not auth_key:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # 这里你可以对 auth 进行解析或验证等操作
    # 例如，如果是 Bearer Token，你可以提取 Token 部分并验证
    # 例如，如果是 Basic Auth，你可以解码并验证用户名密码

    auth_key = auth_key.split(' ')[1]
    return auth_key


async def get_current_user(token: str = Depends(get_auth_header)) -> User:
    """
    # oauth2_scheme -> 从请求头中取到 Authorization 的value
    解析token 获取当前用户对象
    :param token: 登录之后获取到的token
    :return: 当前用户对象
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[
                settings.ALGORITHM])

        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.get(pk=user_id)
    if user is None:
        raise credentials_exception
    return user
