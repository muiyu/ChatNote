# 使用官方 Python 镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY . .

# 复制 api-key.src 文件
COPY api-key.src /app/api-key.src

# 暴露端口
EXPOSE 5000

# 启动后端应用
CMD ["sh", "-c", "set -a && source /app/api-key.src && set +a && python app.py"]