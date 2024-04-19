from fastapi import APIRouter, Depends
from core import deps
from scheams import User_Pydantic
from models import User

user = APIRouter(tags=["用户相关"])


@user.get("/me", summary="当前用户")
async def user_info(user_obj: User = Depends(deps.get_current_user)):
    data = await User_Pydantic.from_tortoise_orm(user_obj)
    return {'resource': data}
