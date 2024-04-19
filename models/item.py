from tortoise import models
from tortoise import fields

from enum import StrEnum


class EnumType(StrEnum):
    income = 'income'
    expenses = 'expenses'


class Item(models.Model):
    user = fields.ForeignKeyField('models.User', related_name="items")
    amount = fields.IntField(description="金额", null=False)
    kind = fields.CharEnumField(enum_type=EnumType, default=None, description="类型", null=True, max_length=10)
    tags = fields.ManyToManyField('models.Tag', related_name='items', description='标签')
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    happen_at = fields.DatetimeField(description="发生时间", null=True)
