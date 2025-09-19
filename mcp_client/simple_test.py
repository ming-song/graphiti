#!/usr/bin/env python3
"""
Simple test script to verify connection to Graphiti MCP Server
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from graphiti_mcp_client import GraphitiMCPClient


async def test_connection():
    """Test connection to the MCP Server."""
    print("Testing connection to Graphiti MCP Server...")

    try:
        async with GraphitiMCPClient(transport="sse", server_url="http://localhost:8000/sse") as client:
            print("Connected to MCP Server")

            # Initialize the client
            await client.initialize()
            print("Client initialized successfully")

            print("Connection test successful!")
            return True

    except Exception as e:
        print(f"Connection test failed: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)