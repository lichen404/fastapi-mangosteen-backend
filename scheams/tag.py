from tortoise.contrib.pydantic import pydantic_model_creator

from models import Tag

Tag_Pydantic = pydantic_model_creator(Tag, name="Tag")
TagIn_Pydantic = pydantic_model_creator(Tag, name="TagIn", exclude_readonly=True,
                                        exclude=('created_at', 'updated_at'))
