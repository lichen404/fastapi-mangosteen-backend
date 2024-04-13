from fastapi import APIRouter
from .endpoints import *


v1 = APIRouter(prefix="/v1")

v1.include_router(login)
v1.include_router(user)
v1.include_router(mail)
v1.include_router(item)
v1.include_router(tag)