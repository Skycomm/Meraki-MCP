#!/usr/bin/env python3
"""
Check all tool names in the MCP server
"""

import os
import sys
import re

def check_tools_in_file(filepath):
    """Check tool names in a Python file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all @app.tool decorators with name parameter
    tool_pattern = r'@app\.tool\([^)]*name\s*=\s*["\']([^"\']+)["\']'
    tools = re.findall(tool_pattern, content, re.DOTALL)
    
    return tools

def main():
    tools_dir = 'server'
    all_tools = []
    
    # Find all tools_*.py files
    for filename in sorted(os.listdir(tools_dir)):
        if filename.startswith('tools_') and filename.endswith('.py'):
            filepath = os.path.join(tools_dir, filename)
            tools = check_tools_in_file(filepath)
            
            for tool in tools:
                all_tools.append((len(tool), tool, filename))
    
    # Sort by length
    all_tools.sort(reverse=True)
    
    print(f"Total tools found: {len(all_tools)}")
    print(f"\nLongest tool names:")
    for i, (length, name, filename) in enumerate(all_tools[:10]):
        print(f"{i+1}. {name} ({length} chars) - {filename}")
    
    # Check if any are over 64 chars
    over_64 = [t for t in all_tools if t[0] > 64]
    if over_64:
        print(f"\n⚠️  Tools with names over 64 characters:")
        for length, name, filename in over_64:
            print(f"  {name} ({length} chars) - {filename}")
    else:
        print("\n✓ No tools with names over 64 characters")
    
    # Show tool at index 277 if it exists
    if len(all_tools) > 277:
        length, name, filename = all_tools[277]
        print(f"\nTool at index 277 (when sorted by length):")
        print(f"  {name} ({length} chars) - {filename}")
    
    # Also show tools around that position
    print(f"\nTools from index 270-280:")
    for i in range(max(0, 270), min(len(all_tools), 281)):
        length, name, filename = all_tools[i]
        print(f"  {i}: {name} ({length} chars)")

if __name__ == '__main__':
    main()