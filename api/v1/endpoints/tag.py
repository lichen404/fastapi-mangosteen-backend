from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from core import deps
from models import Tag
from scheams import TagIn_Pydantic, Tag_Pydantic

tag = APIRouter(tags=["标签相关"])


@tag.get("/tag/{pk}", summary="查询标签")
async def get_tag(pk: int):
    data = await Tag_Pydantic.from_queryset_single(Tag.get(pk=pk))
    return data


@tag.post("/tag", summary="新增标签")
async def movie_create(movie_form: TagIn_Pydantic, user=Depends(deps.get_current_user)):
    data = await Tag_Pydantic.from_tortoise_orm(await Tag.create(user=user, **movie_form.dict()))
    return data


@tag.put("/tag/{pk}", summary="编辑标签", dependencies=[Depends(deps.get_current_user)])
async def movie_update(pk: int, movie_form: TagIn_Pydantic):
    if await Tag.filter(pk=pk).update(**movie_form.dict()):
        return JSONResponse(status_code=200, content="")
    return JSONResponse(content={"msg": "更新失败"}, status_code=400)


@tag.delete("/tag/{pk}", summary="删除标签", dependencies=[Depends(deps.get_current_user)])
async def movie_delete(pk: int):
    if await Tag.filter(pk=pk).delete():
        return JSONResponse(status_code=200, content="")
    return JSONResponse(content={"msg": "删除失败"}, status_code=400)
