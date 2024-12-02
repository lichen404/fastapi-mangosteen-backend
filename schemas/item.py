from tortoise.contrib.pydantic import pydantic_model_creator

from models import Item

Item_Pydantic = pydantic_model_creator(Item, name="Item")
ItemIn_Pydantic = pydantic_model_creator(Item, name="ItemIn", exclude_readonly=True,
                                         exclude=('created_at', 'updated_at'))
