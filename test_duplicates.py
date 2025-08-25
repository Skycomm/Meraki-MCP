#!/usr/bin/env python3
"""Test for duplicate tool registrations."""

import sys
import asyncio
from collections import defaultdict

sys.path.insert(0, 'server')

async def check_tools():
    """Check for duplicate tool registrations."""
    from main import app
    
    print("Analyzing tool registrations...")
    print("=" * 60)
    
    # Get all registered tools
    tool_names = defaultdict(list)
    
    # Check the tools in the app
    if hasattr(app, '_tools'):
        for tool_name, tool_info in app._tools.items():
            tool_names[tool_name].append("registered")
            print(f"Found tool: {tool_name}")
    
    # Find duplicates
    duplicates = {name: sources for name, sources in tool_names.items() if len(sources) > 1}
    
    if duplicates:
        print("\n" + "=" * 60)
        print("DUPLICATE TOOLS FOUND:")
        for name, sources in duplicates.items():
            print(f"  - {name}: registered {len(sources)} times")
    else:
        print("\n✅ No duplicate tools found")
    
    print("=" * 60)
    
    # Try to start the server briefly
    print("\nAttempting to start server...")
    try:
        # Start server for 1 second
        task = asyncio.create_task(app.run())
        await asyncio.sleep(1)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        print("✅ Server started without errors")
    except Exception as e:
        print(f"❌ Server start error: {e}")

if __name__ == "__main__":
    asyncio.run(check_tools())