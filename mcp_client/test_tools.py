#!/usr/bin/env python3
"""
Test script to verify tool calls to Graphiti MCP Server
"""

import asyncio
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from graphiti_mcp_client import GraphitiMCPClient


async def test_tools():
    """Test tool calls to the MCP Server."""
    print("Testing tool calls to Graphiti MCP Server...")

    try:
        async with GraphitiMCPClient(transport="sse", server_url="http://localhost:8000/sse") as client:
            print("Connected to MCP Server")

            # Initialize the client
            await client.initialize()
            print("Client initialized successfully")

            # Test add_memory tool
            result = await client.add_memory(
                name="Test Note",
                episode_body="This is a test note from the MCP client.",
                source="text",
                source_description="test"
            )
            print(f"Add memory result: {result}")

            print("Tool test successful!")
            return True

    except Exception as e:
        print(f"Tool test failed: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_tools())
    sys.exit(0 if result else 1)