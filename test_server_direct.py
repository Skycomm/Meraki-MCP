#!/usr/bin/env python3
"""Test the server directly"""

import asyncio
import json
import sys
from server.main import app

async def test_server():
    """Test the server with a direct call"""
    # List tools
    tools = await app.list_tools()
    print(f"Number of tools: {len(tools)}", file=sys.stderr)
    
    # Show first 5 tools
    for i, tool in enumerate(tools[:5]):
        print(f"Tool {i+1}: {tool.name} - {tool.description}", file=sys.stderr)
    
    # Test get_organizations tool
    try:
        result = await app.call_tool("get_organizations", {})
        print(f"\nget_organizations result type: {type(result)}", file=sys.stderr)
        print(f"Result preview: {str(result)[:200]}...", file=sys.stderr)
    except Exception as e:
        print(f"Error calling get_organizations: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(test_server())