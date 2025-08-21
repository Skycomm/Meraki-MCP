#!/usr/bin/env python3
"""
Extract all MCP tools from the stdio server implementation.
This script parses server/tools_*.py files and generates a unified tool registry.
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

class ToolExtractor:
    def __init__(self, server_path: str):
        self.server_path = Path(server_path)
        self.tools = {}
        
    def extract_all_tools(self) -> Dict[str, Any]:
        """Extract all tools from server/tools_*.py files."""
        tools_files = [
            "tools_organizations.py",
            "tools_networks.py", 
            "tools_devices.py",
            "tools_wireless.py",
            "tools_switch.py",
            "tools_analytics.py",
            "tools_alerts.py",
            "tools_appliance.py",
            "tools_camera.py",
            "tools_sm.py",
            "tools_licensing.py",
            "tools_policy.py",
            "tools_monitoring.py",
            "tools_beta.py",
            "tools_live.py"
        ]
        
        for file_name in tools_files:
            file_path = self.server_path / "server" / file_name
            if file_path.exists():
                print(f"Extracting from {file_name}...")
                self._extract_from_file(file_path)
            else:
                print(f"Warning: {file_name} not found")
                
        return self.tools
    
    def _extract_from_file(self, file_path: Path):
        """Extract tools from a single file."""
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Find all @app.tool decorators and their functions
        tool_pattern = r'@app\.tool\(\s*name\s*=\s*"([^"]+)".*?\)\s*def\s+(\w+)\s*\((.*?)\):\s*"""(.*?)"""'
        matches = re.findall(tool_pattern, content, re.DOTALL)
        
        for match in matches:
            tool_name = match[0]
            func_name = match[1]
            params = match[2]
            docstring = match[3].strip()
            
            # Extract the function body
            func_start = content.find(f'def {func_name}')
            if func_start == -1:
                continue
                
            # Find the end of the function (next def or end of file)
            next_def = content.find('\n    @app.tool', func_start + 1)
            next_func = content.find('\ndef ', func_start + 1)
            
            if next_def == -1:
                next_def = len(content)
            if next_func == -1:
                next_func = len(content)
                
            func_end = min(next_def, next_func)
            func_body = content[func_start:func_end].strip()
            
            # Parse parameters
            param_list = self._parse_parameters(params)
            
            self.tools[tool_name] = {
                'function_name': func_name,
                'parameters': param_list,
                'docstring': docstring,
                'body': func_body,
                'file': file_path.name
            }
            
    def _parse_parameters(self, params_str: str) -> List[Dict[str, Any]]:
        """Parse function parameters."""
        params = []
        if not params_str.strip():
            return params
            
        # Split by comma but respect nested parentheses
        param_parts = []
        current = ""
        paren_count = 0
        
        for char in params_str:
            if char == ',' and paren_count == 0:
                param_parts.append(current.strip())
                current = ""
            else:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                current += char
                
        if current.strip():
            param_parts.append(current.strip())
            
        for param in param_parts:
            if ':' in param:
                name, type_str = param.split(':', 1)
                name = name.strip()
                type_str = type_str.strip()
                
                # Check for default value
                default = None
                if '=' in type_str:
                    type_str, default_str = type_str.split('=', 1)
                    type_str = type_str.strip()
                    default = default_str.strip()
                    
                params.append({
                    'name': name,
                    'type': type_str,
                    'default': default,
                    'required': default is None
                })
            else:
                # No type annotation
                if '=' in param:
                    name, default = param.split('=', 1)
                    params.append({
                        'name': name.strip(),
                        'type': 'Any',
                        'default': default.strip(),
                        'required': False
                    })
                else:
                    params.append({
                        'name': param.strip(),
                        'type': 'Any',
                        'default': None,
                        'required': True
                    })
                    
        return params
    
    def generate_tool_registry(self, output_path: str):
        """Generate the unified tool registry file."""
        with open(output_path, 'w') as f:
            f.write('"""\nAuto-generated tool registry from stdio server.\nContains all 97 MCP tools with implementations.\n"""\n\n')
            f.write('from typing import Dict, Any, List, Optional\n')
            f.write('import json\n\n')
            f.write('# Import meraki_client - will be set by the server\n')
            f.write('meraki_client = None\n\n')
            f.write('def set_meraki_client(client):\n')
            f.write('    """Set the global meraki_client."""\n')
            f.write('    global meraki_client\n')
            f.write('    meraki_client = client\n\n')
            
            # Generate all tool functions
            for tool_name, tool_info in self.tools.items():
                f.write(f"\n# From {tool_info['file']}\n")
                
                # Convert to async function
                func_body = tool_info['body']
                func_body = func_body.replace('def ', 'async def ', 1)
                
                # Replace meraki_client calls with await
                func_body = re.sub(r'meraki_client\.(\w+)\(', r'await meraki_client.\1(', func_body)
                
                # Write the function
                f.write(func_body)
                f.write('\n\n')
                
            # Generate the ALL_TOOLS dictionary
            f.write('\n# Tool registry\n')
            f.write('ALL_TOOLS = {\n')
            for tool_name, tool_info in self.tools.items():
                f.write(f'    "{tool_name}": {tool_info["function_name"]},\n')
            f.write('}\n\n')
            
            # Generate tool metadata
            f.write('# Tool metadata for MCP protocol\n')
            f.write('TOOL_METADATA = {\n')
            for tool_name, tool_info in self.tools.items():
                params_json = json.dumps(tool_info['parameters'])
                docstring_escaped = tool_info['docstring'].replace('"', '\\"').replace('\n', '\\n')
                f.write(f'    "{tool_name}": {{\n')
                f.write(f'        "description": "{docstring_escaped}",\n')
                f.write(f'        "parameters": {params_json}\n')
                f.write(f'    }},\n')
            f.write('}\n')

if __name__ == "__main__":
    # Get the parent directory (cisco-meraki-mcp-server-tvi)
    base_path = Path(__file__).parent.parent
    
    extractor = ToolExtractor(base_path)
    tools = extractor.extract_all_tools()
    
    print(f"\nExtracted {len(tools)} tools")
    
    # Generate the tool registry
    output_path = Path(__file__).parent / "src" / "tool_registry.py"
    extractor.generate_tool_registry(str(output_path))
    
    print(f"Generated tool registry at: {output_path}")
    
    # Print summary
    print("\nTool categories:")
    categories = {}
    for tool_name, tool_info in tools.items():
        category = tool_info['file'].replace('tools_', '').replace('.py', '')
        if category not in categories:
            categories[category] = []
        categories[category].append(tool_name)
        
    for category, tool_list in sorted(categories.items()):
        print(f"  {category}: {len(tool_list)} tools")