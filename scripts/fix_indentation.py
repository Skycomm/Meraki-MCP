#!/usr/bin/env python3
"""
Fix indentation issues in consolidated files.
The consolidation script left functions with incorrect indentation.
"""

import re

def fix_file_indentation(filepath):
    """Fix indentation in a consolidated module file."""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find the register function and everything after it
    register_pattern = r'(def register_\w+_tools\(mcp_app, meraki\):[^@]*)'
    
    # Split at register function
    parts = re.split(register_pattern, content, 1)
    if len(parts) != 3:
        print(f"  Could not find register function pattern")
        return
    
    header = parts[0]
    register_func_start = parts[1] 
    tools_section = parts[2]
    
    # Fix tool function indentation - they should be at base level
    # Remove the 4-space indentation that was added during consolidation
    fixed_tools = []
    lines = tools_section.split('\n')
    
    for line in lines:
        if line.startswith('    @app.tool('):
            # Start of a new tool - remove extra indentation
            fixed_tools.append(line[4:])  # Remove 4 spaces
        elif line.startswith('        def ') and '_(' in line:
            # Tool function definition - remove extra indentation
            fixed_tools.append(line[4:])  # Remove 4 spaces
        elif line.startswith('        ') and len(line.strip()) > 0:
            # Tool body content - remove extra indentation
            fixed_tools.append(line[4:])  # Remove 4 spaces
        else:
            # Keep other lines as-is (empty lines, etc.)
            fixed_tools.append(line)
    
    # Reconstruct the file
    new_content = header + register_func_start + '\n'.join(fixed_tools)
    
    # Write back to file
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    print(f"  ✅ Fixed indentation in {filepath}")

def main():
    """Fix indentation in all consolidated files."""
    files = [
        'server/tools_organizations.py',
        'server/tools_wireless.py', 
        'server/tools_appliance.py'
    ]
    
    for filepath in files:
        try:
            fix_file_indentation(filepath)
        except Exception as e:
            print(f"  ❌ Error fixing {filepath}: {e}")

if __name__ == '__main__':
    main()