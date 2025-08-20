#!/usr/bin/env python3
"""
Comprehensive tool inventory for Meraki MCP Server
Lists all registered tools and their details
"""

import os
import re
import ast
from typing import Dict, List, Tuple

def extract_tools_from_file(filepath: str) -> List[Dict[str, str]]:
    """Extract tool definitions from a Python file."""
    tools = []
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Pattern 1: @app.tool() decorator with explicit name
        pattern1 = r'@app\.tool\(\s*name\s*=\s*["\']([^"\']+)["\'].*?\)\s*def\s+(\w+)'
        matches1 = re.findall(pattern1, content, re.DOTALL)
        
        for tool_name, func_name in matches1:
            # Find the docstring
            func_pattern = f'def {func_name}.*?"""(.*?)"""'
            doc_match = re.search(func_pattern, content, re.DOTALL)
            docstring = doc_match.group(1).strip() if doc_match else ""
            
            tools.append({
                'name': tool_name,
                'function': func_name,
                'description': docstring.split('\n')[0] if docstring else "",
                'category': os.path.basename(filepath).replace('tools_', '').replace('.py', '')
            })
        
        # Pattern 2: @mcp_app.tool() decorator (newer style)
        pattern2 = r'@mcp_app\.tool\(\)\s*def\s+(\w+).*?"""(.*?)"""'
        matches2 = re.findall(pattern2, content, re.DOTALL)
        
        for func_name, docstring in matches2:
            tools.append({
                'name': func_name,
                'function': func_name,
                'description': docstring.strip().split('\n')[0],
                'category': os.path.basename(filepath).replace('tools_', '').replace('.py', '')
            })
        
        # Pattern 3: app.tool() registration in register function
        pattern3 = r'app\.tool\(\)\((\w+)\)'
        matches3 = re.findall(pattern3, content)
        
        for func_name in matches3:
            # Find the function definition and docstring
            func_pattern = f'def {func_name}.*?"""(.*?)"""'
            doc_match = re.search(func_pattern, content, re.DOTALL)
            if doc_match:
                docstring = doc_match.group(1).strip()
                tools.append({
                    'name': func_name,
                    'function': func_name,
                    'description': docstring.split('\n')[0],
                    'category': os.path.basename(filepath).replace('tools_', '').replace('.py', '')
                })
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    
    return tools

def main():
    """Generate complete tool inventory."""
    all_tools = []
    tools_by_category = {}
    
    # Scan all tool files
    server_dir = 'server'
    for filename in sorted(os.listdir(server_dir)):
        if filename.startswith('tools_') and filename.endswith('.py'):
            filepath = os.path.join(server_dir, filename)
            tools = extract_tools_from_file(filepath)
            
            if tools:
                category = filename.replace('tools_', '').replace('.py', '')
                tools_by_category[category] = tools
                all_tools.extend(tools)
    
    # Generate report
    print("# Meraki MCP Server - Complete Tool Inventory")
    print(f"\nTotal Tools: {len(all_tools)}")
    print(f"Categories: {len(tools_by_category)}")
    print("\n## Tools by Category\n")
    
    # Sort categories by tool count
    sorted_categories = sorted(tools_by_category.items(), 
                             key=lambda x: len(x[1]), 
                             reverse=True)
    
    for category, tools in sorted_categories:
        print(f"\n### {category.replace('_', ' ').title()} ({len(tools)} tools)")
        print()
        
        for tool in sorted(tools, key=lambda x: x['name']):
            print(f"- **{tool['name']}**")
            if tool['description']:
                print(f"  - {tool['description']}")
    
    # Summary statistics
    print("\n## Summary Statistics\n")
    print(f"- Total Tools: {len(all_tools)}")
    print(f"- Categories: {len(tools_by_category)}")
    print(f"- Average Tools per Category: {len(all_tools) / len(tools_by_category):.1f}")
    
    # Category breakdown
    print("\n## Category Breakdown\n")
    for category, tools in sorted_categories:
        print(f"- {category}: {len(tools)} tools")
    
    # Export to JSON for further processing
    import json
    with open('tool_inventory.json', 'w') as f:
        json.dump({
            'total_tools': len(all_tools),
            'categories': len(tools_by_category),
            'tools': all_tools,
            'by_category': {k: [t['name'] for t in v] 
                          for k, v in tools_by_category.items()}
        }, f, indent=2)
    
    print("\n✅ Tool inventory exported to tool_inventory.json")

if __name__ == "__main__":
    main()