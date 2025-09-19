# Graphiti MCP Server 工具使用指南

## 概述

Graphiti MCP Server 提供了一套完整的工具来管理时态感知的知识图谱。本文档详细介绍了如何使用两个客户端应用程序来演示所有可用的 MCP 工具。

**Server 地址**: `http://localhost:8000/sse`

## 可用工具

### 1. 内存管理工具
- **add_memory** - 添加记忆片段（支持文本、JSON、消息格式）
- **delete_episode** - 删除指定的记忆片段
- **get_episodes** - 获取最近的记忆片段

### 2. 搜索工具
- **search_memory_nodes** - 搜索知识图谱中的节点
- **search_memory_facts** - 搜索实体间的关系事实

### 3. 图谱管理工具
- **get_entity_edge** - 根据 UUID 获取实体边
- **delete_entity_edge** - 删除实体边
- **clear_graph** - 清空整个图谱

### 4. 状态监控
- **get_status** - 获取服务器状态和 Neo4j 连接信息

## 客户端应用

### 1. 命令行客户端 (mcp_client/)

#### 安装和设置
```bash
cd mcp_client
uv sync
```

#### 基本使用
```bash
# 运行完整演示
uv run python graphiti_mcp_client.py --demo

# 指定服务器地址
uv run python graphiti_mcp_client.py --transport sse --server-url http://localhost:8000/sse --demo
```

#### API 使用示例
```python
from graphiti_mcp_client import GraphitiMCPClient

async with GraphitiMCPClient(transport="sse", server_url="http://localhost:8000/sse") as client:
    await client.initialize()

    # 获取服务器状态
    status = await client.get_status()

    # 添加记忆
    result = await client.add_memory(
        name="Example Note",
        episode_body="This is an example note.",
        source="text",
        source_description="example"
    )

    # 搜索节点
    nodes = await client.search_memory_nodes(query="example", max_nodes=5)

    # 搜索关系
    facts = await client.search_memory_facts(query="example", max_facts=5)
```

#### 测试状态
✅ **可用** - 基本功能正常，JSON 序列化问题已修复

### 2. Web 界面客户端 (mcp_client_web/)

#### 安装和设置
```bash
cd mcp_client_web
uv add flask[async] mcp
```

#### 启动 Web 应用
```bash
uv run python app.py
```

Web 应用将在 `http://localhost:5000` 启动

#### 功能页面
- **首页** (`/`) - 服务器状态检查和快速导航
- **内存管理** (`/memory`) - 添加记忆片段
- **搜索** (`/search`) - 搜索节点和关系
- **片段查看** (`/episodes`) - 查看最近的记忆片段

#### API 端点测试
```bash
# 测试添加记忆
curl -X POST http://localhost:5000/api/add_memory \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Memory", "episode_body": "Test content", "source": "text"}'

# 测试获取片段
curl -X POST http://localhost:5000/api/get_episodes \
  -H "Content-Type: application/json" \
  -d '{"last_n": 5}'

# 测试搜索节点（需要有效的 OpenAI API key）
curl -X POST http://localhost:5000/api/search_nodes \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "max_nodes": 5}'
```

#### 测试状态
✅ **完全可用** - 所有工具都能正确返回 JSON 响应

## 完整演示流程

### 步骤 1: 启动 MCP Server
确保 Graphiti MCP Server 运行在 `http://localhost:8000/sse`

### 步骤 2: 测试命令行客户端
```bash
cd mcp_client
uv run python graphiti_mcp_client.py --demo
```

### 步骤 3: 启动 Web 界面
```bash
cd mcp_client_web
uv run python app.py
```

### 步骤 4: 通过 Web 界面测试所有工具
1. 访问 `http://localhost:5000`
2. 点击 "Check Server Status" 验证连接
3. 使用各个页面测试不同工具：
   - 添加不同格式的记忆片段
   - 搜索知识图谱中的节点和关系
   - 查看和管理记忆片段

## 环境要求

- Python 3.10+
- uv 包管理器
- 运行中的 Graphiti MCP Server
- Neo4j 数据库连接

## 已知问题

1. **MCP Server API 配置**:
   - 当前 MCP Server 只支持 OpenAI API，尽管已配置 Google Gemini API key
   - 搜索和记忆处理功能需要有效的 OpenAI API key
   - 记忆被加入处理队列但无法完成处理（缺少有效 LLM）

2. **记忆处理状态**:
   - `add_memory` 成功加入队列：`"Episode 'XXX' queued for processing (position: 1)"`
   - `get_episodes` 返回空，因为记忆未完成 LLM 处理
   - 需要有效的 API key 来完成实体提取和关系生成

3. **依赖管理**: Web 客户端需要 `flask[async]` 和 `mcp` 依赖，已通过 uv 解决
4. **异步资源清理**: MCP 客户端异步连接清理问题已修复

## 修复记录

- ✅ **JSON 序列化问题**: 添加 `_convert_result_to_dict` 函数处理 `CallToolResult` 对象
- ✅ **Flask 异步支持**: 安装 `flask[async]` 支持异步视图
- ✅ **异步资源清理**: 改进 MCP 客户端的 `__aexit__` 方法错误处理

## 配置选项

### 环境变量
- `MCP_SERVER_URL` - MCP 服务器地址（默认: http://localhost:8000/sse）
- `MCP_TRANSPORT` - 传输方法（默认: sse）
- `FLASK_ENV` - Flask 环境（默认: production）

两个客户端都能够完整演示 MCP Server 提供的工具功能，Web 界面提供了更直观的交互体验。