# 使用官方的 Python 作为基础镜像
FROM python:3.12


# 安装Poetry
RUN pip install poetry -i https://mirrors.aliyun.com/pypi/simple

# 设置工作目录
WORKDIR /app

# 将项目文件添加到工作目录中
COPY . /app/

# 配置镜像源
RUN poetry self add poetry-plugin-pypi-mirror

ENV POETRY_PYPI_MIRROR_URL=https://mirrors.aliyun.com/pypi/simple

# 使用Poetry安装依赖项
RUN poetry install

# 添加初始化脚本
COPY init.sh /usr/local/bin/init.sh

# 设置脚本权限
RUN chmod +x /usr/local/bin/init.sh

# 启动应用
CMD ["/usr/local/bin/init.sh"]
