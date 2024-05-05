# 使用官方的 Python 作为基础镜像
FROM python:3.12


# 安装Poetry
RUN pip install poetry

# 设置工作目录
WORKDIR /app

# 将项目文件添加到工作目录中
COPY . /app/

# 使用Poetry安装依赖项
RUN poetry install

# 启动应用
CMD ["poetry", "run", "python", "main.py"]
