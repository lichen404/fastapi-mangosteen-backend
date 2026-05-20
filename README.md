# 介绍
>仿 [山竹记账全栈版](https://xiedaimala.com/courses/89c07499-0174-40e3-81ce-a9eca822de40) Rails后端
使用(Python): FastAPI + Tortoise ORM + PostgreSQL (原先为 SQLite, 已迁移支持 Postgres)  



## 功能清单
- [x] 登录
- [x] 发送验证码
- [x] 添加标签
- [x] 删除标签
- [x] 修改标签
- [x] item 新增
- [x] item 查询
- [x] 图表接口

## 优化
- [x] 利用 redis 实现验证码过期清除
- [x] 数据库金额字段优化为 Decimal
- [x] 统计接口性能优化 (数据库聚合)

## 接口文档地址
[文档](http://123.57.27.189:3000/docs)

## Docker 部署 (使用 Postgres + Redis)
1. 安装Docker-compose
2. `git clone https://github.com/lichen404/fastapi-mangosteen-backend.git`
3. `cd fastapi-mangosteen-backend`
4. 创建 .env 文件
  ```bash
  SECRET_KEY=secret
  MAIL_PASSWORD=qq邮箱申请的smtp授权码
  # 生产环境 Docker 部署时，POSTGRES_HOST 会在 docker-compose.yml 中自动覆盖为 'postgres'
  # 本地开发时请设置为 localhost 或 127.0.0.1
  POSTGRES_HOST=localhost
  POSTGRES_PORT=5432
  POSTGRES_DB=mangosteen
  POSTGRES_USER=mangosteen
  POSTGRES_PASSWORD=mangosteen
  ```
5. 执行 `docker-compose up -d --build`
   > 注意：容器启动时会自动执行 `aerich upgrade` 进行数据库迁移。
6. 访问 http://localhost:3000/docs

### 本地开发使用 Postgres
若本地需要使用 Postgres 而不是 SQLite，可设置环境变量或在 `.env` 中添加：
```bash
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=mangosteen
POSTGRES_USER=mangosteen
POSTGRES_PASSWORD=mangosteen
```
### 迁移 (Aerich)
首次初始化（若之前是 SQLite，建议重新建库）：
```bash
poetry run aerich init -t settings.TORTOISE_ORM
poetry run aerich init-db
```
之后模型变更：
```bash
poetry run aerich migrate
poetry run aerich upgrade
```

### 前端对接
访问 `http://localhost:3000/openapi.json` 获取接口文档，可将其保存为 `openapi.json` 提供给前端 Copilot 使用。



