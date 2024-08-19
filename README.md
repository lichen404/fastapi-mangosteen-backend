# 介绍
>仿 [山竹记账全栈版](https://xiedaimala.com/courses/89c07499-0174-40e3-81ce-a9eca822de40) Rails后端
使用(Python): FastAPI + Tortoise ORM + SQLite  



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

## 接口文档地址
[文档](http://123.57.27.189:3000/docs)

## Docker 部署
1. 安装Docker-compose
2. `git clone https://github.com/lichen404/fastapi-mangosteen-backend.git`
3. `cd fastapi-mangosteen-backend`
4. 创建 .env 文件
  ```bash
  SECRET_KEY=secret
  MAIL_PASSWORD=qq邮箱申请的smtp授权码
  ```
5. 执行 `docker-compose up -d`
6. 访问 http://localhost:3000/docs


