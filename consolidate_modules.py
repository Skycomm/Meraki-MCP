#!/usr/bin/env python3
"""
Consolidate split module files into single SDK-matching modules.
This will combine:
- All tools_wireless*.py files into tools_wireless.py
- All tools_organizations*.py files into tools_organizations.py  
- All tools_appliance*.py files into tools_appliance.py
"""

import re
from pathlib import Path

def extract_tools_from_file(filepath):
    """Extract tool definitions from a Python file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all tool definitions
    tool_pattern = r'(@app\.tool\([^)]+\)\s*def\s+\w+[^@]*?)(?=@app\.tool|$)'
    tools = re.findall(tool_pattern, content, re.DOTALL)
    
    return tools

def extract_imports_from_file(filepath):
    """Extract unique imports from a file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Get all import statements before the first function/class definition
    lines = content.split('\n')
    imports = []
    for line in lines:
        if line.startswith(('import ', 'from ')):
            imports.append(line)
        elif line.startswith(('def ', 'class ', '@')):
            break
    
    return imports

def consolidate_category(category_name, file_patterns, output_file):
    """Consolidate multiple module files into one."""
    print(f"\nConsolidating {category_name} modules...")
    
    base_path = Path('server')
    all_tools = []
    all_imports = set()
    
    # Process each file pattern
    for pattern in file_patterns:
        for filepath in sorted(base_path.glob(pattern)):
            if filepath.exists():
                print(f"  Processing {filepath.name}...")
                tools = extract_tools_from_file(filepath)
                imports = extract_imports_from_file(filepath)
                
                all_tools.extend(tools)
                all_imports.update(imports)
                
                print(f"    Found {len(tools)} tools")
    
    # Create consolidated file content
    content = f'''"""
{category_name.title()} tools for Cisco Meraki MCP server.
Consolidated from multiple modules to match SDK structure.
"""

'''
    
    # Add imports (deduplicated and sorted)
    standard_imports = sorted([i for i in all_imports if not i.startswith('from server')])
    local_imports = sorted([i for i in all_imports if i.startswith('from server')])
    
    for imp in standard_imports:
        if imp and 'tools_' not in imp:  # Skip imports from other tools modules
            content += imp + '\n'
    
    content += '\n# Global references to be set by register function\n'
    content += 'app = None\n'
    content += 'meraki_client = None\n\n'
    
    # Add register function
    func_name = f'register_{category_name}_tools'
    content += f'''def {func_name}(mcp_app, meraki):
    """
    Register {category_name} tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
'''
    
    # Add all tools
    for tool in all_tools:
        # Indent the tool definition
        indented_tool = '\n    '.join(tool.split('\n'))
        content += '    ' + indented_tool + '\n'
    
    # Write consolidated file
    output_path = base_path / output_file
    print(f"  Writing {len(all_tools)} tools to {output_file}")
    
    # Create backup of original if it exists
    if output_path.exists():
        backup_path = output_path.with_suffix('.py.backup')
        print(f"  Backing up original to {backup_path.name}")
        output_path.rename(backup_path)
    
    with open(output_path, 'w') as f:
        f.write(content)
    
    print(f"  ✅ Consolidated {len(all_tools)} tools into {output_file}")
    
    return len(all_tools)

def main():
    """Main consolidation process."""
    print("🔧 Consolidating modules to match SDK structure")
    print("=" * 60)
    
    # Define consolidation rules
    consolidations = [
        {
            'category': 'wireless',
            'patterns': ['tools_wireless*.py'],
            'output': 'tools_wireless_consolidated.py'  # Temporary name to avoid conflicts
        },
        {
            'category': 'organizations', 
            'patterns': ['tools_organizations*.py'],
            'output': 'tools_organizations_consolidated.py'
        },
        {
            'category': 'appliance',
            'patterns': ['tools_appliance*.py'],
            'output': 'tools_appliance_consolidated.py'
        }
    ]
    
    total_tools = 0
    for config in consolidations:
        count = consolidate_category(
            config['category'],
            config['patterns'],
            config['output']
        )
        total_tools += count
    
    print("\n" + "=" * 60)
    print(f"✅ Consolidation complete! Total tools: {total_tools}")
    print("\nNext steps:")
    print("1. Review the consolidated files")
    print("2. Rename _consolidated.py files to replace originals")
    print("3. Update main.py imports")
    print("4. Delete the old split files")

if __name__ == '__main__':
    main()