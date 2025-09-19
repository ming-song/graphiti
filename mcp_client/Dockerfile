# MCP Client CLI Dockerfile
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
    uv pip install --system mcp httpx httpx-sse

# 复制应用代码
COPY . .

# 设置权限
RUN chown -R app:app /app

# 切换到应用用户
USER app

# 设置环境变量
ENV MCP_SERVER_URL=http://graphiti-mcp:8000/sse
ENV MCP_TRANSPORT=sse

# 默认命令 - 运行演示
CMD ["python", "graphiti_mcp_client.py", "--demo"]