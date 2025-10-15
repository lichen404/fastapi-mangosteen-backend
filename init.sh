#!/bin/bash

poetry run aerich init -t settings.TORTOISE_ORM
# 初始化数据库
echo "初始化数据库..."
poetry run aerich init-db

# 启动应用
echo "启动应用..."
poetry run python main.py