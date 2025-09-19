#!/usr/bin/env python3
"""
Example usage of the Graphiti MCP Client
"""

import asyncio
from graphiti_mcp_client import GraphitiMCPClient


async def example_usage():
    """Example of how to use the Graphiti MCP Client."""

    # Connect to the MCP Server using SSE transport
    async with GraphitiMCPClient(transport="sse", server_url="http://localhost:8000/sse") as client:
        # Initialize the client
        await client.initialize()

        # Get server status
        status = await client.get_status()
        print(f"Server Status: {status}")

        # Add a memory episode
        result = await client.add_memory(
            name="Example Note",
            episode_body="This is an example note added through the MCP client.",
            source="text",
            source_description="example"
        )
        print(f"Add Memory Result: {result}")

        # Search for nodes
        nodes = await client.search_memory_nodes(
            query="example",
            max_nodes=5
        )
        print(f"Search Nodes Result: {nodes}")

        # Search for facts
        facts = await client.search_memory_facts(
            query="example",
            max_facts=5
        )
        print(f"Search Facts Result: {facts}")


if __name__ == "__main__":
    asyncio.run(example_usage())