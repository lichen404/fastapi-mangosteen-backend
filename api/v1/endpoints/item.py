from datetime import datetime
from typing import List, Literal
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from core import deps
from models import Item, Tag
from models.item import EnumType

item = APIRouter(tags=["Item相关"])


@item.get("/items", summary="Item 列表", )
async def movie_list(happened_before: datetime, happened_after: datetime, limit: int = 25, page: int = 1,
                     current_user=Depends(deps.get_current_user)):
    items_with_tags = []
    skip = (page - 1) * limit
    items = await (
        Item.filter(user=current_user, happen_at__lt=happened_before, happen_at__gt=happened_after).all().offset(
            skip).limit(limit).order_by('-id')
        .prefetch_related('tags'))
    for i in items:
        tags = await i.tags.all()
        items_with_tags.append({'amount': i.amount, 'id': i.pk, 'tags': tags, 'kind': i.kind, 'happen_at': i.happen_at})
    data = {
        "total": await Item.filter(user=current_user).all().count(),
        "items": items_with_tags
    }
    return data


class BalanceOut(BaseModel):
    expenses: int
    income: int
    balance: int


@item.get("/balance", summary="收支", response_model=BalanceOut)
async def movie_list(happened_before: datetime,
                     happened_after: datetime,
                     current_user=Depends(deps.get_current_user)):
    balance = {'income': 0, 'expenses': 0, 'balance': 0}
    items = await Item.filter(user=current_user, happen_at__lt=happened_before, happen_at__gt=happened_after).all()
    for i in items:
        if i.kind == 'expenses':
            balance['expenses'] += i.amount
            balance['balance'] -= i.amount
        else:
            balance['income'] += i.amount
            balance['balance'] += i.amount

    return balance


class SummaryOut(BaseModel):
    groups: List
    total: int


@item.get("/summary", summary="收支", response_model=SummaryOut)
async def movie_list(happened_before: datetime,
                     happened_after: datetime,
                     kind: Literal['income', 'expenses'] = 'income',
                     group_by: Literal['tag_id', 'happen_at'] = "tag_id",
                     current_user=Depends(deps.get_current_user)):
    result = {}
    items = await (
        Item.filter(user=current_user, happen_at__lt=happened_before, happen_at__gt=happened_after, kind=kind)
        .all()).prefetch_related('tags')
    total = 0
    for i in items:
        if group_by == "tag_id":
            for t in await i.tags.all():
                if result.get(t.pk) is None:
                    result[t.pk] = {
                        'tag_id': t.pk,
                        'tag': t,
                        'amount': i.amount
                    }
                else:
                    result[t.pk]['amount'] += i.amount
        else:
            key = i.happen_at.strftime("%F")
            if result.get(key) is None:
                result[key] = {
                    'amount': i.amount,
                    'happen_at': key
                }
            else:
                result[key]['amount'] += i.amount
        total += i.amount

    return {'groups': list(result.values()), 'total': total}


class ItemModel(BaseModel):
    amount: int
    tag_ids: List[int] = []
    kind: EnumType
    happen_at: datetime


@item.post("/item", summary="新增item")
async def movie_create(movie_form: ItemModel, user=Depends(deps.get_current_user)):
    data = await Item.create(user=user, **movie_form.dict())
    tags = await Tag.filter(id__in=movie_form.tag_ids)
    await data.tags.add(*tags)
    return data
