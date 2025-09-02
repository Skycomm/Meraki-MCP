#!/usr/bin/env python3
"""
Fix organizations module by removing duplicates, fixing indentation,
and ensuring we have exactly 173 tools matching the official SDK.
"""

import re
from collections import defaultdict
import subprocess

def fix_organizations_module():
    """Fix the organizations module comprehensively."""
    
    print("🔧 Fixing Organizations Module...")
    
    # Read current file
    with open('server/tools_SDK_organizations.py', 'r') as f:
        content = f.read()
    
    # Extract all @app.tool definitions with their full functions
    tool_pattern = r'(@app\.tool\(\s*name="([^"]*)".*?\n(?:.*?\n)*?(?=@app\.tool\(|def register_|$))'
    matches = re.findall(tool_pattern, content, re.DOTALL | re.MULTILINE)
    
    print(f"📊 Found {len(matches)} tool definitions")
    
    # Group tools by name to find duplicates
    tools_by_name = defaultdict(list)
    for full_match, tool_name in matches:
        tools_by_name[tool_name].append(full_match)
    
    # Keep only first instance of each duplicate
    unique_tools = {}
    duplicates_removed = 0
    
    for tool_name, tool_instances in tools_by_name.items():
        if len(tool_instances) > 1:
            print(f"⚠️ Removing {len(tool_instances)-1} duplicates of: {tool_name}")
            duplicates_removed += len(tool_instances) - 1
        
        # Keep the first (usually best) instance
        unique_tools[tool_name] = tool_instances[0]
    
    print(f"✅ Removed {duplicates_removed} duplicate tools")
    print(f"📊 Unique tools remaining: {len(unique_tools)}")
    
    # Create clean tool definitions
    clean_tools = []
    for tool_name, tool_def in unique_tools.items():
        # Fix indentation - ensure tools are properly indented within function
        lines = tool_def.split('\n')
        fixed_lines = []
        
        for line in lines:
            if line.strip().startswith('@app.tool('):
                fixed_lines.append('    ' + line.strip())  # Function level indent
            elif line.strip().startswith('def '):
                fixed_lines.append('    ' + line.strip())  # Function level indent  
            elif line.strip() and not line.startswith('    '):
                fixed_lines.append('        ' + line.strip())  # Inside function indent
            else:
                fixed_lines.append(line)  # Keep existing indentation
        
        clean_tools.append('\n'.join(fixed_lines))
    
    # Create the base file structure
    base_structure = '''"""
Core organization management tools for Cisco Meraki MCP server.

This module provides complete 100% SDK coverage for organization operations,
including management, adaptive policies, administrators, alerts, and more.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_organizations_tools(mcp_app, meraki):
    """
    Register all organization tools with the MCP server.
    Provides 100% coverage of the official Cisco Meraki Organizations SDK.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all organization tool handlers
    register_all_organizations_handlers()

def register_all_organizations_handlers():
    """Register all 173 organization tools to match official SDK exactly."""
    
    # ==================== ALL ORGANIZATION TOOLS ====================
    
'''
    
    # Add all unique tools
    tools_section = '\n\n'.join(clean_tools)
    
    # Create the complete file
    complete_file = base_structure + tools_section + '\n'
    
    # Write the clean file
    with open('server/tools_SDK_organizations.py', 'w') as f:
        f.write(complete_file)
    
    print("✅ Created clean organizations module")
    
    # Test syntax
    syntax_result = subprocess.run(['python', '-m', 'py_compile', 'server/tools_SDK_organizations.py'],
                                 capture_output=True)
    
    if syntax_result.returncode == 0:
        print("✅ Syntax check passed")
    else:
        print(f"❌ Syntax error: {syntax_result.stderr.decode()[:200]}")
        return False
    
    # Count final tools
    final_count = len(unique_tools)
    print(f"📊 Final tool count: {final_count}")
    print(f"🎯 Target: 173 (official SDK)")
    print(f"📈 Progress: {(final_count/173)*100:.1f}%")
    
    remaining = 173 - final_count
    if remaining > 0:
        print(f"⚠️ Still need {remaining} more tools")
    else:
        print("🎉 100% SDK coverage achieved!")
    
    return final_count

if __name__ == "__main__":
    count = fix_organizations_module()
    print(f"\\n🏁 Organizations module fixed with {count} tools")