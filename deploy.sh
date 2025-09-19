#!/bin/bash

# Graphiti MCP Server 一键部署脚本
# 支持完整的开发和生产环境部署

set -e

COMPOSE_FILE="docker-compose.full.yml"
ENV_FILE="mcp_server/.env"

show_help() {
    echo "Graphiti MCP Server 一键部署脚本"
    echo ""
    echo "使用方法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  up        启动所有服务 (默认)"
    echo "  down      停止所有服务"
    echo "  restart   重启所有服务"
    echo "  status    检查服务状态"
    echo "  logs      查看服务日志"
    echo "  demo      启动包含CLI演示的完整环境"
    echo "  build     重新构建镜像"
    echo ""
    echo "选项:"
    echo "  --prod    生产模式 (禁用调试)"
    echo "  --dev     开发模式 (启用调试，默认)"
    echo ""
    echo "示例:"
    echo "  $0                    # 启动基础服务"
    echo "  $0 demo               # 启动包含CLI演示"
    echo "  $0 up --prod          # 生产模式启动"
    echo "  $0 logs graphiti-mcp  # 查看MCP Server日志"
    echo "  $0 build              # 重新构建镜像"
    echo ""
    echo "服务端口:"
    echo "  - Neo4j Web界面:  http://localhost:\${NEO4J_HTTP_PORT:-7474}"
    echo "  - MCP Server:     http://localhost:\${MCP_SERVER_PORT:-8000}"
    echo "  - Web客户端:      http://localhost:\${WEB_CLIENT_PORT:-5000}"
    echo ""
    echo "端口配置:"
    echo "  export NEO4J_HTTP_PORT=8474    # 修改Neo4j Web端口"
    echo "  export MCP_SERVER_PORT=9000    # 修改MCP Server端口"
    echo "  export WEB_CLIENT_PORT=6000    # 修改Web客户端端口"
}

check_prerequisites() {
    echo "🔧 检查环境依赖..."

    # 检查Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker未安装，请先安装Docker"
        exit 1
    fi

    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose未安装，请先安装"
        exit 1
    fi

    # 检查.env文件
    if [ ! -f "$ENV_FILE" ]; then
        echo "⚠️  未找到环境配置文件: $ENV_FILE"
        echo "   请确保配置了必要的API密钥"
    else
        echo "✅ 环境配置文件存在"
    fi

    echo "✅ 环境依赖检查完成"
}

build_images() {
    echo "🏗️  构建Docker镜像..."
    docker-compose -f $COMPOSE_FILE build
    echo "✅ 镜像构建完成"
}

start_services() {
    local mode=${1:-dev}
    local with_demo=${2:-false}

    echo "🚀 启动Graphiti MCP服务..."

    # 设置环境
    if [ "$mode" = "prod" ]; then
        export FLASK_DEBUG=0
        export FLASK_ENV=production
        echo "📦 生产模式启动"
    else
        export FLASK_DEBUG=1
        export FLASK_ENV=development
        echo "🔧 开发模式启动"
    fi

    # 选择profiles
    if [ "$with_demo" = "true" ]; then
        echo "🎭 启动完整环境 (包含CLI演示)"
        docker-compose -f $COMPOSE_FILE --profile demo up -d
    else
        echo "🎯 启动基础服务"
        docker-compose -f $COMPOSE_FILE up -d neo4j graphiti-mcp mcp-web-client
    fi

    echo ""
    echo "⏳ 等待服务启动..."
    sleep 5

    # 检查服务状态
    check_service_status
}

stop_services() {
    echo "🛑 停止所有服务..."
    docker-compose -f $COMPOSE_FILE down
    echo "✅ 服务已停止"
}

check_service_status() {
    echo "📊 服务状态："
    echo ""

    # 检查容器状态
    docker-compose -f $COMPOSE_FILE ps

    echo ""
    echo "🌐 服务地址："

    # 检查Neo4j
    if curl -s -m 2 http://localhost:7474 > /dev/null 2>&1; then
        echo "✅ Neo4j Web界面:  http://localhost:7474"
    else
        echo "❌ Neo4j Web界面:  http://localhost:7474 (未运行)"
    fi

    # 检查MCP Server
    if curl -s -m 2 http://localhost:8000/sse | grep -q "endpoint" 2>/dev/null; then
        echo "✅ MCP Server:     http://localhost:8000"
    else
        echo "❌ MCP Server:     http://localhost:8000 (未运行)"
    fi

    # 检查Web客户端
    if curl -s -m 2 http://localhost:5000 | grep -q "html\|Graphiti" 2>/dev/null; then
        echo "✅ Web客户端:      http://localhost:5000"
    else
        echo "❌ Web客户端:      http://localhost:5000 (未运行)"
    fi
}

show_logs() {
    local service=${1:-}
    if [ -z "$service" ]; then
        echo "📋 显示所有服务日志..."
        docker-compose -f $COMPOSE_FILE logs --tail=50 -f
    else
        echo "📋 显示 $service 服务日志..."
        docker-compose -f $COMPOSE_FILE logs --tail=50 -f "$service"
    fi
}

# 主逻辑
ACTION=${1:-up}
MODE="dev"
WITH_DEMO=false

# 解析参数
shift || true
while [[ $# -gt 0 ]]; do
    case $1 in
        --prod)
            MODE="prod"
            shift
            ;;
        --dev)
            MODE="dev"
            shift
            ;;
        --demo)
            WITH_DEMO=true
            shift
            ;;
        *)
            SERVICE_NAME=$1
            shift
            ;;
    esac
done

# 执行对应操作
case $ACTION in
    up|start)
        check_prerequisites
        build_images
        start_services $MODE $WITH_DEMO
        ;;
    down|stop)
        stop_services
        ;;
    restart)
        echo "🔄 重启服务..."
        stop_services
        sleep 2
        check_prerequisites
        start_services $MODE $WITH_DEMO
        ;;
    status)
        check_service_status
        ;;
    logs)
        show_logs $SERVICE_NAME
        ;;
    demo)
        echo "🎭 启动演示环境..."
        check_prerequisites
        build_images
        start_services $MODE true
        ;;
    build)
        check_prerequisites
        build_images
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ 未知命令: $ACTION"
        echo ""
        show_help
        exit 1
        ;;
esac