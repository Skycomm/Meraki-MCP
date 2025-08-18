#!/usr/bin/env python3
"""
Extract all tool functions from original MCP server and convert to hybrid format
"""

import os
import re
from pathlib import Path

def extract_tools_from_file(filepath):
    """Extract all @app.tool decorated functions from a file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    tools = []
    
    # Find all @app.tool decorators
    decorator_pattern = r'@app\.tool\([^)]+\)'
    decorator_matches = list(re.finditer(decorator_pattern, content))
    
    for i, dec_match in enumerate(decorator_matches):
        # Get the decorator content
        decorator = dec_match.group(0)
        
        # Extract name and description from decorator
        name_match = re.search(r'name="([^"]+)"', decorator)
        desc_match = re.search(r'description="([^"]+)"', decorator)
        
        if not name_match:
            continue
            
        tool_name = name_match.group(1)
        description = desc_match.group(1) if desc_match else ""
        
        # Find the function definition after this decorator
        func_start = dec_match.end()
        func_pattern = r'def\s+(\w+)\((.*?)\):\s*"""(.*?)"""'
        func_match = re.search(func_pattern, content[func_start:func_start+2000], re.DOTALL)
        
        if not func_match:
            continue
            
        func_name = func_match.group(1)
        params = func_match.group(2)
        docstring = func_match.group(3).strip()
        
        # Get the function body
        body_start = func_start + func_match.end()
        
        # Find the end of this function (next decorator, next function, or end of file)
        if i + 1 < len(decorator_matches):
            body_end = decorator_matches[i + 1].start()
        else:
            # Look for next function or end of file
            next_func = re.search(r'\n(def\s+\w+|class\s+\w+)', content[body_start:])
            if next_func:
                body_end = body_start + next_func.start()
            else:
                body_end = len(content)
        
        body = content[body_start:body_end].strip()
        
        # Clean up body - remove trailing whitespace and extra newlines
        body_lines = body.split('\n')
        # Remove empty lines at the end
        while body_lines and not body_lines[-1].strip():
            body_lines.pop()
        body = '\n'.join(body_lines)
        
        tools.append({
            'name': tool_name,
            'func_name': func_name,
            'params': params,
            'docstring': docstring,
            'body': body,
            'description': description
        })
    
    return tools

def convert_to_async_function(tool):
    """Convert tool to async function format"""
    # Clean up parameters
    params = tool['params'].strip()
    if params and not params.endswith(','):
        params = params.rstrip()
    
    # Convert body to use await for meraki_client calls
    body = tool['body']
    body = re.sub(r'meraki_client\.(\w+)\(', r'await meraki_client.\1(', body)
    
    # Add proper indentation to the entire body
    body_lines = body.split('\n')
    indented_body = []
    for line in body_lines:
        if line.strip():  # Non-empty line
            indented_body.append('    ' + line)
        else:
            indented_body.append('')
    body = '\n'.join(indented_body)
    
    # Build the async function - use the tool name from decorator, not function name
    func_def = f"""async def {tool['name']}({params}) -> str:
    \"\"\"{tool['description']}\"\"\"
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
{body}"""
    
    return func_def

def main():
    server_dir = Path("/Users/david/docker/cisco-meraki-mcp-server-tvi/server")
    tools_files = list(server_dir.glob("tools_*.py"))
    
    all_tools = []
    
    for file in sorted(tools_files):
        print(f"Processing {file.name}...")
        tools = extract_tools_from_file(file)
        for tool in tools:
            tool['module'] = file.stem
        all_tools.extend(tools)
    
    print(f"\nTotal tools found: {len(all_tools)}")
    
    # Generate the tools code
    output = []
    output.append("# Tool implementations (converted from MCP decorators)")
    
    # Group by module
    from itertools import groupby
    for module, group in groupby(all_tools, key=lambda x: x['module']):
        output.append(f"\n# {module.replace('tools_', '').title()} Tools")
        for tool in group:
            output.append("")
            output.append(convert_to_async_function(tool))
    
    # Generate tools mapping
    output.append("\n# Tools mapping for execute_tool endpoint")
    output.append("MERAKI_TOOLS = {")
    for tool in all_tools:
        params_list = [p.strip().split(':')[0].strip() for p in tool['params'].split(',') if p.strip()]
        if params_list:
            output.append(f'    "{tool["name"]}": lambda: {tool["name"]}(**request.arguments),')
        else:
            output.append(f'    "{tool["name"]}": {tool["name"]},')
    output.append("}")
    
    # Write to output file
    with open("hybrid_tools.py", "w") as f:
        f.write('\n'.join(output))
    
    print("\nTools extracted to hybrid_tools.py")
    
    # Print summary
    print("\nTools by module:")
    module_counts = {}
    for tool in all_tools:
        module = tool['module'].replace('tools_', '')
        module_counts[module] = module_counts.get(module, 0) + 1
    
    for module, count in sorted(module_counts.items()):
        print(f"  {module}: {count} tools")

if __name__ == "__main__":
    main()