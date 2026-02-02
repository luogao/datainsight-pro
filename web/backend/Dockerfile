FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制并安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 FastAPI 和相关依赖
RUN pip install fastapi uvicorn[standard] python-multipart

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p /app/web/backend/uploads /app/outputs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "web.backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
