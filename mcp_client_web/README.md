# Graphiti MCP Client Web Interface

A web-based interface for interacting with the Graphiti MCP Server.

## Features

- Web-based GUI for all Graphiti MCP tools
- Add memory episodes (text, JSON, message)
- Search nodes and facts in the knowledge graph
- View episodes
- Server status monitoring

## Prerequisites

- Python 3.7+
- Graphiti MCP Server running at `http://localhost:8000/sse`
- Flask

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure the Graphiti MCP Client library is available:
   ```bash
   # Navigate to the mcp_client directory
   cd ../mcp_client
   pip install -e .
   ```

## Configuration

The web interface can be configured using environment variables:

- `MCP_SERVER_URL` - URL of the MCP server (default: http://localhost:8000/sse)
- `MCP_TRANSPORT` - Transport method (default: sse)
- `FLASK_ENV` - Flask environment (default: production)
- `FLASK_APP` - Flask app module (default: app.py)

## Running the Web Interface

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

## Usage

### Home Page
- Check server status
- Quick navigation to other sections

### Memory Management
- Add new episodes to the knowledge graph
- Supports text, JSON, and message formats

### Search
- Search for nodes in the knowledge graph
- Search for facts (relationships between entities)

### Episodes
- View recent episodes
- Filter by group ID

## API Endpoints

- `GET /` - Home page
- `GET /memory` - Memory management page
- `GET /search` - Search page
- `GET /episodes` - Episodes page
- `GET /api/status` - Server status
- `POST /api/add_memory` - Add memory
- `POST /api/search_nodes` - Search nodes
- `POST /api/search_facts` - Search facts
- `POST /api/get_episodes` - Get episodes

## Development

To run in development mode:
```bash
export FLASK_ENV=development
python app.py
```

## License

This project is licensed under the MIT License.