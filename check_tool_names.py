#!/usr/bin/env python3
"""
Script to check all tool names across the Cisco Meraki MCP Server codebase
to ensure they meet the 64-character limit for MCP/Claude Desktop compatibility.
"""

import os
import re
import glob
from collections import defaultdict

def extract_tool_names_from_file(file_path):
    """Extract all tool names from a Python file containing @app.tool decorators."""
    tool_names = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match @app.tool decorators with name= parameter
        pattern = r'@app\.tool\s*\(\s*name\s*=\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        for match in matches:
            tool_names.append(match)
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return tool_names

def main():
    """Main function to check all tool names across the codebase."""
    
    # Define paths to check
    server_dir = "/Users/david/docker/cisco-meraki-mcp-server-tvi/server"
    
    # Get all SDK and Custom tool files
    sdk_files = glob.glob(os.path.join(server_dir, "tools_SDK_*.py"))
    custom_files = glob.glob(os.path.join(server_dir, "tools_Custom_*.py"))
    
    all_files = sdk_files + custom_files
    
    print("🔍 CISCO MERAKI MCP SERVER - TOOL NAME LENGTH ANALYSIS")
    print("=" * 60)
    print(f"📁 Checking {len(all_files)} tool files...")
    print()
    
    all_tool_names = []
    tools_by_file = {}
    long_names = []
    
    # Process each file
    for file_path in sorted(all_files):
        file_name = os.path.basename(file_path)
        tool_names = extract_tool_names_from_file(file_path)
        
        if tool_names:
            tools_by_file[file_name] = tool_names
            all_tool_names.extend(tool_names)
            
            # Check for long names in this file
            file_long_names = [(name, len(name)) for name in tool_names if len(name) >= 64]
            if file_long_names:
                long_names.extend([(file_name, name, length) for name, length in file_long_names])
    
    # Summary statistics
    total_tools = len(all_tool_names)
    max_length = max(len(name) for name in all_tool_names) if all_tool_names else 0
    
    print(f"📊 SUMMARY STATISTICS")
    print(f"   Total tool files: {len(all_files)}")
    print(f"   Total tools found: {total_tools}")
    print(f"   Maximum name length: {max_length} characters")
    print()
    
    # Report any names that exceed the limit
    if long_names:
        print("❌ TOOLS EXCEEDING 64-CHARACTER LIMIT:")
        print("-" * 60)
        for file_name, tool_name, length in sorted(long_names, key=lambda x: x[2], reverse=True):
            print(f"📁 {file_name}")
            print(f"   🛠️  {tool_name}")
            print(f"   📏 {length} characters (exceeds limit by {length - 64})")
            print()
    else:
        print("✅ ALL TOOL NAMES ARE WITHIN 64-CHARACTER LIMIT!")
        print()
    
    # Show longest names (top 10)
    print("📏 LONGEST TOOL NAMES (Top 10):")
    print("-" * 60)
    name_lengths = [(name, len(name)) for name in all_tool_names]
    name_lengths.sort(key=lambda x: x[1], reverse=True)
    
    for i, (name, length) in enumerate(name_lengths[:10], 1):
        status = "❌" if length >= 64 else "✅"
        print(f"{i:2}. {status} {name}")
        print(f"    📏 {length} characters")
        print()
    
    # Show distribution by file
    print("📂 TOOLS PER FILE:")
    print("-" * 60)
    for file_name in sorted(tools_by_file.keys()):
        tool_count = len(tools_by_file[file_name])
        max_len_in_file = max(len(name) for name in tools_by_file[file_name])
        status = "❌" if any(len(name) >= 64 for name in tools_by_file[file_name]) else "✅"
        print(f"{status} {file_name}: {tool_count} tools (max length: {max_len_in_file})")
    
    print()
    print("🎯 CONCLUSION:")
    if long_names:
        print(f"❌ Found {len(long_names)} tool names exceeding 64-character limit!")
        print("   These tools will fail in Claude Desktop and must be shortened.")
    else:
        print("✅ All tool names are MCP/Claude Desktop compatible!")
    
    return len(long_names) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)