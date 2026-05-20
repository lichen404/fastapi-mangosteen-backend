#!/bin/bash

# 应用数据库迁移
# 注意：由于我们将 migrations 文件夹打包进了镜像，
# 无论是第一次部署（空数据库）还是后续更新，
# aerich upgrade 都会自动判断并应用所需的迁移脚本。
# - 空数据库：应用所有迁移（0_init.py, 1_update.py ...）
# - 现有数据库：只应用新增的迁移
echo "应用数据库迁移..."
poetry run aerich upgrade

# 启动应用
echo "启动应用..."
poetry run python main.py