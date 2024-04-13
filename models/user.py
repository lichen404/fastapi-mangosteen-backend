from tortoise import models
from tortoise import fields


class User(models.Model):
    email = fields.CharField(max_length=128, null=False, description="账号", unique=True)
