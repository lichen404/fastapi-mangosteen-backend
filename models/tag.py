from tortoise import models
from tortoise import fields


class Tag(models.Model):
    user = fields.ForeignKeyField('models.User', related_name="tags")
    name = fields.CharField(max_length=50, description="名称", null=False)
    sign = fields.CharField(max_length=10, description="标志", null=False)
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    # auto_now 参数无效
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
