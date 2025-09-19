# MCP Client Web Dockerfile
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 安装uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin:$PATH"

# 创建应用用户
RUN groupadd -r app && useradd -r -d /app -g app app

# 复制依赖文件
COPY pyproject.toml uv.lock* ./

# 安装Python依赖
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system flask[async] mcp httpx httpx-sse

# 复制应用代码
COPY . .

# 设置权限
RUN chown -R app:app /app

# 切换到应用用户
USER app

# 设置环境变量
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
ENV MCP_SERVER_URL=http://graphiti-mcp:8000/sse
ENV MCP_TRANSPORT=sse

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "5000"]