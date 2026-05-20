import asyncio
from datetime import datetime
from decimal import Decimal
from models.item import EnumType
from typing import List, Literal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from tortoise.functions import Sum
from core import deps
from models import Item, Tag

item = APIRouter(tags=["Item相关"])


@item.get("/items", summary="Item 列表", )
async def item_list(happened_before: datetime, happened_after: datetime, limit: int = 25, page: int = 1,
                    current_user=Depends(deps.get_current_user)):
    if (happened_before - happened_after).days > 366:
        raise HTTPException(status_code=400, detail="时间间隔不能超过1年")
    skip = (page - 1) * limit
    base_filter = Item.filter(user=current_user, happen_at__lt=happened_before, happen_at__gt=happened_after)
    items, count = await asyncio.gather(
        base_filter.offset(skip).limit(limit).order_by('-id').prefetch_related('tags'),
        base_filter.count()
    )
    items_with_tags = []
    for i in items:
        items_with_tags.append({'amount': i.amount, 'id': i.pk, 'tags': list(i.tags), 'kind': i.kind, 'happen_at': i.happen_at})
    data = {
        "pager": {
            "count": count,
            'page': str(page),
            'per_page': limit
        },
        "resources": items_with_tags
    }
    return data


class BalanceOut(BaseModel):
    expenses: float
    income: float
    balance: float


@item.get("/items/balance", summary="收支", response_model=BalanceOut)
async def items_balance(happened_before: datetime,
                        happened_after: datetime,
                        current_user=Depends(deps.get_current_user)):
    if (happened_before - happened_after).days > 366:
        raise HTTPException(status_code=400, detail="时间间隔不能超过1年")
    base_filter = Item.filter(user=current_user, happen_at__lt=happened_before, happen_at__gt=happened_after)
    income_rows, expenses_rows = await asyncio.gather(
        base_filter.filter(kind='income').annotate(total=Sum('amount')).values('total'),
        base_filter.filter(kind='expenses').annotate(total=Sum('amount')).values('total'),
    )
    income = income_rows[0]['total'] or Decimal(0)
    expenses = expenses_rows[0]['total'] or Decimal(0)
    return {
        'income': float(income),
        'expenses': float(expenses),
        'balance': float(income - expenses)
    }


class SummaryOut(BaseModel):
    groups: List
    total: float


@item.get("/items/summary", summary="收支", response_model=SummaryOut)
async def summary(happened_before: datetime,
                  happened_after: datetime,
                  kind: Literal['income', 'expenses'] = 'income',
                  group_by: Literal['tag_id', 'happen_at'] = "tag_id",
                  current_user=Depends(deps.get_current_user)):
    result = {}
    if (happened_before - happened_after).days > 366:
        raise HTTPException(status_code=400, detail="时间间隔不能超过1年")
    items = await (
        Item.filter(user=current_user, happen_at__lt=happened_before, happen_at__gt=happened_after, kind=kind)
        .prefetch_related('tags'))
    total = Decimal(0)
    for i in items:
        if group_by == "tag_id":
            for t in list(i.tags):
                if result.get(t.pk) is None:
                    result[t.pk] = {
                        'tag_id': t.pk,
                        'tag': {
                            'name': t.name,
                            'sign': t.sign
                        },
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
    amount: Decimal
    tag_ids: List[int] = []
    kind: EnumType
    happen_at: datetime


@item.post("/items", summary="新增item")
async def item_create(item_form: ItemModel, user=Depends(deps.get_current_user)):
    data = await Item.create(user=user, **item_form.model_dump())
    tags = await Tag.filter(id__in=item_form.tag_ids)
    await data.tags.add(*tags)
    return data
