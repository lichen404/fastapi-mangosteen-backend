from typing import Literal
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from core import deps
from models import Tag
from scheams import TagIn_Pydantic, Tag_Pydantic

tag = APIRouter(tags=["标签相关"])


@tag.get("/tags/{pk}", summary="查询标签")
async def get_tag(pk: int):
    data = await Tag_Pydantic.from_queryset_single(Tag.get(pk=pk))
    return {'resource': data}


@tag.get("/tags", summary="标签列表", )
async def item_list(kind: Literal['expenses', 'income'], limit: int = 25, page: int = 1,
                    current_user=Depends(deps.get_current_user)):
    skip = (page - 1) * limit
    tags = await (Tag.filter(user=current_user, kind=kind).all().offset(skip).limit(limit).order_by('-id'))
    data = {
        "pager": {
            "count": await Tag.filter(user=current_user, kind=kind).all().count(),
            'page': str(page),
            'per_page': limit
        },
        "resources": tags
    }
    return data


@tag.post("/tags", summary="新增标签")
async def tag_create(tag_from: TagIn_Pydantic, user=Depends(deps.get_current_user)):
    data = await Tag_Pydantic.from_tortoise_orm(await Tag.create(user=user, **tag_from.dict()))
    return data


@tag.put("/tags/{pk}", summary="编辑标签", dependencies=[Depends(deps.get_current_user)])
async def tag_update(pk: int, tag_form: TagIn_Pydantic):
    if await Tag.filter(pk=pk).update(**tag_form.dict()):
        m = await Tag.filter(pk=pk).first()
        # 调用 .save 方法才能触发 auto_now
        await m.save()
        return JSONResponse(status_code=200, content="")
    return JSONResponse(content={"msg": "更新失败"}, status_code=400)


@tag.delete("/tags/{pk}", summary="删除标签", dependencies=[Depends(deps.get_current_user)])
async def tag_delete(pk: int, with_items: bool = False):
    if with_items:
        t = await Tag.filter(pk=pk).first().prefetch_related('items')
        items = await t.items.all()
        for item in items:
            await item.delete()
        await t.delete()
        return JSONResponse(status_code=200, content="")
    else:
        if await Tag.filter(pk=pk).delete():
            return JSONResponse(status_code=200, content="")
    return JSONResponse(content={"msg": "删除失败"}, status_code=400)
