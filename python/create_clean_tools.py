#!/usr/bin/env python3
"""Create a clean version of tools by re-extracting with better parsing"""

import os
import re
import ast
from pathlib import Path

def extract_tool_info_ast(filepath):
    """Extract tool information using AST parsing for better accuracy"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    tools = []
    
    # Find all @app.tool decorators and their functions
    decorator_pattern = r'@app\.tool\(\s*name="([^"]+)"[^)]*description="([^"]+)"[^)]*\)\s*def\s+(\w+)\((.*?)\):'
    
    for match in re.finditer(decorator_pattern, content, re.DOTALL):
        tool_name = match.group(1)
        description = match.group(2)
        func_name = match.group(3)
        params = match.group(4).strip()
        
        # Find the function body
        func_start = match.end()
        
        # Find the end of the function (next @app.tool or def)
        next_func = re.search(r'(?=@app\.tool|def\s+register_)', content[func_start:])
        if next_func:
            func_end = func_start + next_func.start()
        else:
            func_end = len(content)
        
        # Extract function body
        func_body = content[func_start:func_end]
        
        # Extract docstring
        docstring_match = re.match(r'\s*"""(.*?)"""', func_body, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1).strip()
            # Remove docstring from body
            func_body = func_body[docstring_match.end():]
        else:
            docstring = description
        
        tools.append({
            'name': tool_name,
            'func_name': func_name,
            'description': description,
            'params': params,
            'docstring': docstring,
            'body': func_body.strip()
        })
    
    return tools

def create_async_function(tool):
    """Create a properly formatted async function"""
    params = tool['params']
    
    # Build function
    lines = [
        f"async def {tool['name']}({params}) -> str:",
        f'    """{tool["description"]}"""',
        '    if not meraki_client:',
        '        return "Error: Meraki client not initialized"',
        '    '
    ]
    
    # Check if body already has try/except
    body = tool['body'].strip()
    has_try = body.startswith('try:')
    
    if not has_try:
        lines.append('    try:')
    
    # Add body lines with proper indentation
    body_lines = body.split('\n')
    for line in body_lines:
        if line.strip():
            # Convert meraki_client calls to async
            line = re.sub(r'meraki_client\.(\w+)\(', r'await meraki_client.\1(', line)
            
            # Adjust indentation based on whether we added try
            if has_try:
                lines.append('    ' + line)
            else:
                lines.append('        ' + line)
    
    # Ensure we have exception handling if we added try
    if not has_try and 'except' not in tool['body']:
        lines.extend([
            '    except Exception as e:',
            '        return f"Error: {str(e)}"'
        ])
    
    return '\n'.join(lines)

def main():
    server_dir = Path("/Users/david/docker/cisco-meraki-mcp-server-tvi/server")
    tools_files = sorted(server_dir.glob("tools_*.py"))
    
    output = ['"""All 97 Meraki tools ported from the original MCP server"""',
              '',
              '# We\'ll get meraki_client from the importing module',
              'meraki_client = None',
              '',
              'def set_meraki_client(client):',
              '    """Set the global meraki_client"""',
              '    global meraki_client',
              '    meraki_client = client',
              '',
              '# Tool implementations (converted from MCP decorators)',
              '']
    
    all_tools = []
    
    for file in tools_files:
        print(f"Processing {file.name}...")
        tools = extract_tool_info_ast(file)
        
        if tools:
            module_name = file.stem.replace('tools_', '').title()
            output.append(f'# {module_name} Tools')
            output.append('')
            
            for tool in tools:
                all_tools.append(tool['name'])
                output.append(create_async_function(tool))
                output.append('')
    
    # Create ALL_TOOLS dict
    output.extend([
        '# Dictionary of all tools for easy access',
        'ALL_TOOLS = {',
    ])
    
    for tool_name in sorted(all_tools):
        output.append(f'    "{tool_name}": {tool_name},')
    
    output.append('}')
    
    # Write output
    with open('src/meraki_tools.py', 'w') as f:
        f.write('\n'.join(output))
    
    print(f"\nCreated clean tools file with {len(all_tools)} tools")

if __name__ == "__main__":
    main()