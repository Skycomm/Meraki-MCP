#!/usr/bin/env python3
"""
Count and verify wireless tools are registered correctly.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def count_tools():
    """Count all wireless tools."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()
            
            # Get all tools
            tools = await session.list_tools()
            
            # Filter wireless tools
            wireless_tools = [t for t in tools.tools if 'wireless' in t.name]
            
            print(f"Total wireless tools: {len(wireless_tools)}")
            
            # Group by category
            categories = {}
            for tool in wireless_tools:
                parts = tool.name.split('_')
                if 'ssid' in tool.name:
                    category = 'SSID'
                elif 'client' in tool.name:
                    category = 'Client'
                elif 'device' in tool.name:
                    category = 'Device'
                elif 'organization' in tool.name:
                    category = 'Organization'
                elif 'history' in tool.name or 'stats' in tool.name:
                    category = 'Analytics'
                else:
                    category = 'Network'
                
                if category not in categories:
                    categories[category] = []
                categories[category].append(tool.name)
            
            print("\nTools by category:")
            for cat, tools in sorted(categories.items()):
                print(f"  {cat}: {len(tools)} tools")
            
            return len(wireless_tools)

if __name__ == "__main__":
    count = asyncio.run(count_tools())
    print(f"\n✅ Successfully registered {count} wireless tools")
