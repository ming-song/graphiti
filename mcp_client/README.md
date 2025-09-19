# Graphiti MCP Client

A lightweight Python client to demonstrate all features and tools of the Graphiti MCP Server.

## Features

This client demonstrates all the available tools from the Graphiti MCP Server:

1. **add_memory** - Add episodes to memory (text, JSON, or message formats)
2. **search_memory_nodes** - Search for nodes in the knowledge graph
3. **search_memory_facts** - Search for facts (edges between entities)
4. **delete_entity_edge** - Delete an entity edge from the graph
5. **delete_episode** - Delete an episode from the graph
6. **get_entity_edge** - Get an entity edge by UUID
7. **get_episodes** - Get recent episodes for a group
8. **clear_graph** - Clear all data from the graph
9. **get_status** - Get the status of the Graphiti MCP server (resource)

## Installation

1. Install `uv` if you don't have it already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   cd mcp_client
   uv sync
   ```

## Usage

### Running the Demo

To run the demo client that demonstrates all features:

```bash
uv run graphiti_mcp_client.py --demo
```

### Using SSE Transport (Default)

The client connects to the MCP Server using SSE transport by default:

```bash
uv run graphiti_mcp_client.py --transport sse --server-url http://localhost:8000/sse --demo
```

### Command Line Options

- `--transport`: Transport method ("sse" or "stdio", default: "sse")
- `--server-url`: Server URL for SSE transport (default: http://localhost:8000/sse)
- `--demo`: Run the demo client

## API

The client provides a Python class `GraphitiMCPClient` with methods for each tool:

```python
from graphiti_mcp_client import GraphitiMCPClient

async with GraphitiMCPClient() as client:
    await client.initialize()
    status = await client.get_status()
    print(status)
```

## Requirements

- Python 3.10 or higher
- Access to a running Graphiti MCP Server
- MCP-compatible client library

## License

This project is licensed under the MIT License.