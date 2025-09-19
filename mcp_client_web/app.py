#!/usr/bin/env python3
"""
Web interface for Graphiti MCP Client
"""

import os
import sys
from pathlib import Path

# Add the parent directory to Python path to import the MCP client
sys.path.insert(0, str(Path(__file__).parent.parent))
# Add the mcp_client directory to Python path
sys.path.insert(0, '/home/songm/code/graphiti/mcp_client')

from flask import Flask, render_template, request, jsonify
from graphiti_mcp_client import GraphitiMCPClient
import asyncio
import json

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# Configuration
MCP_SERVER_URL = os.environ.get('MCP_SERVER_URL', 'http://localhost:8000/sse')
MCP_TRANSPORT = os.environ.get('MCP_TRANSPORT', 'sse')

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html', server_url=MCP_SERVER_URL)

@app.route('/memory')
def memory():
    """Memory management page."""
    return render_template('memory.html')

@app.route('/search')
def search():
    """Search page."""
    return render_template('search.html')

@app.route('/episodes')
def episodes():
    """Episodes page."""
    return render_template('episodes.html')

@app.route('/api/status')
async def get_status():
    """Get server status."""
    try:
        async with GraphitiMCPClient(transport=MCP_TRANSPORT, server_url=MCP_SERVER_URL) as client:
            await client.initialize()
            status = await client.get_status()
            return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/add_memory', methods=['POST'])
async def add_memory():
    """Add memory to the graph."""
    try:
        data = request.get_json()
        name = data.get('name', '')
        episode_body = data.get('episode_body', '')
        source = data.get('source', 'text')
        source_description = data.get('source_description', '')
        group_id = data.get('group_id', None)
        uuid = data.get('uuid', None)

        async with GraphitiMCPClient(transport=MCP_TRANSPORT, server_url=MCP_SERVER_URL) as client:
            await client.initialize()
            result = await client.add_memory(
                name=name,
                episode_body=episode_body,
                source=source,
                source_description=source_description,
                group_id=group_id,
                uuid=uuid
            )
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search_nodes', methods=['POST'])
async def search_nodes():
    """Search for nodes in the graph."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        group_ids = data.get('group_ids', None)
        max_nodes = data.get('max_nodes', 10)
        center_node_uuid = data.get('center_node_uuid', None)
        entity = data.get('entity', '')

        async with GraphitiMCPClient(transport=MCP_TRANSPORT, server_url=MCP_SERVER_URL) as client:
            await client.initialize()
            result = await client.search_memory_nodes(
                query=query,
                group_ids=group_ids,
                max_nodes=max_nodes,
                center_node_uuid=center_node_uuid,
                entity=entity
            )
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search_facts', methods=['POST'])
async def search_facts():
    """Search for facts in the graph."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        group_ids = data.get('group_ids', None)
        max_facts = data.get('max_facts', 10)
        center_node_uuid = data.get('center_node_uuid', None)

        async with GraphitiMCPClient(transport=MCP_TRANSPORT, server_url=MCP_SERVER_URL) as client:
            await client.initialize()
            result = await client.search_memory_facts(
                query=query,
                group_ids=group_ids,
                max_facts=max_facts,
                center_node_uuid=center_node_uuid
            )
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_episodes', methods=['POST'])
async def get_episodes():
    """Get episodes from the graph."""
    try:
        data = request.get_json()
        group_id = data.get('group_id', None)
        last_n = data.get('last_n', 10)

        async with GraphitiMCPClient(transport=MCP_TRANSPORT, server_url=MCP_SERVER_URL) as client:
            await client.initialize()
            result = await client.get_episodes(
                group_id=group_id,
                last_n=last_n
            )
            return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_async(coro):
    """Run async function in a new event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

# Wrap async routes with sync versions for Flask
@app.route('/api/status')
def get_status_sync():
    return run_async(get_status())

@app.route('/api/add_memory', methods=['POST'])
def add_memory_sync():
    return run_async(add_memory())

@app.route('/api/search_nodes', methods=['POST'])
def search_nodes_sync():
    return run_async(search_nodes())

@app.route('/api/search_facts', methods=['POST'])
def search_facts_sync():
    return run_async(search_facts())

@app.route('/api/get_episodes', methods=['POST'])
def get_episodes_sync():
    return run_async(get_episodes())

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Graphiti MCP Web Client')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')

    args = parser.parse_args()

    # 从环境变量读取配置
    import os
    debug = args.debug or os.getenv('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')

    print(f"🌐 Starting Graphiti MCP Web Client on {args.host}:{args.port}")
    print(f"   MCP Server URL: {os.getenv('MCP_SERVER_URL', 'http://localhost:8000/sse')}")
    print(f"   Debug mode: {debug}")

    app.run(debug=debug, host=args.host, port=args.port)