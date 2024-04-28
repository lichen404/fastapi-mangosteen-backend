# 第一个阶段：构建阶段
FROM python:3.12 AS builder


# 设置工作目录
WORKDIR /app

# 将依赖项清单文件添加到工作目录
COPY requirements.txt /app/requirements.txt

# 使用pip安装依赖项
RUN pip install  --no-cache-dir --upgrade -r  /app/requirements.txt


# 第二个阶段：运行阶段
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制从构建阶段复制的依赖项
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# 将项目文件添加到工作目录
COPY . /app/

EXPOSE 8000

# 启动应用
CMD ["python", "main.py"]

