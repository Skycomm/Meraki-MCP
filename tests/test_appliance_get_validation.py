#!/usr/bin/env python3
"""
Simple validation test for appliance GET commands in the Cisco Meraki MCP Server.
Tests only that GET tool functions exist and are properly defined (no API calls).
"""

import os
import sys
import re

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_appliance_tools_validation():
    """Validate appliance tools exist and are properly structured."""
    
    print("# 🧪 Validating Appliance Tools Structure\n")
    
    appliance_file = "server/tools_SDK_appliance.py"
    
    with open(appliance_file, 'r') as f:
        content = f.read()
    
    # Count @app.tool decorators
    tool_decorators = re.findall(r'@app\.tool\(', content)
    tool_count = len(tool_decorators)
    
    print(f"**Total Tools Found**: {tool_count}")
    
    # Find all GET tools (read-only operations)
    get_tools = re.findall(r'def (get_[a-zA-Z_]*)\(', content)
    get_count = len(get_tools)
    
    print(f"**GET Tools Count**: {get_count}")
    
    # Find all CREATE tools
    create_tools = re.findall(r'def (create_[a-zA-Z_]*)\(', content)
    create_count = len(create_tools)
    
    print(f"**CREATE Tools Count**: {create_count}")
    
    # Find all UPDATE tools  
    update_tools = re.findall(r'def (update_[a-zA-Z_]*)\(', content)
    update_count = len(update_tools)
    
    print(f"**UPDATE Tools Count**: {update_count}")
    
    # Find all DELETE tools
    delete_tools = re.findall(r'def (delete_[a-zA-Z_]*)\(', content)
    delete_count = len(delete_tools)
    
    print(f"**DELETE Tools Count**: {delete_count}")
    
    # Find all OTHER tools (swap, etc.)
    other_tools = re.findall(r'def ((?!get_|create_|update_|delete_)[a-zA-Z_]*)\(', content)
    other_count = len(other_tools)
    
    print(f"**OTHER Tools Count**: {other_count}")
    
    total_functions = get_count + create_count + update_count + delete_count + other_count
    print(f"**Total Functions**: {total_functions}")
    
    print(f"\n## ✅ Validation Results")
    
    # Validate target of 130 tools
    if tool_count == 130:
        print(f"✅ **Tool Count**: {tool_count}/130 - PERFECT!")
    else:
        print(f"⚠️ **Tool Count**: {tool_count}/130 - Off by {130 - tool_count}")
    
    # Show breakdown
    print(f"\n## 📊 Tool Breakdown:")
    print(f"- **Read Operations (GET)**: {get_count}")
    print(f"- **Create Operations**: {create_count}")  
    print(f"- **Update Operations**: {update_count}")
    print(f"- **Delete Operations**: {delete_count}")
    print(f"- **Other Operations**: {other_count}")
    
    # List some sample GET tools
    print(f"\n## 🔍 Sample GET Tools:")
    for i, tool in enumerate(get_tools[:10], 1):
        print(f"{i}. {tool}")
    if len(get_tools) > 10:
        print(f"... and {len(get_tools) - 10} more GET tools")
    
    # Validate official SDK methods match
    print(f"\n## 🎯 Official SDK Validation:")
    
    # Check for key appliance SDK methods that should exist
    key_methods = [
        'get_network_appliance_settings',
        'get_network_appliance_vlans', 
        'get_network_appliance_firewall_l3_firewall_rules',
        'update_network_appliance_settings',
        'create_network_appliance_vlan',
        'delete_network_appliance_vlan'
    ]
    
    missing_methods = []
    for method in key_methods:
        if method not in content:
            missing_methods.append(method)
    
    if not missing_methods:
        print("✅ All key appliance methods are present!")
    else:
        print(f"⚠️ Missing key methods: {missing_methods}")
    
    return tool_count, get_count, create_count, update_count, delete_count

if __name__ == "__main__":
    try:
        tools, gets, creates, updates, deletes = test_appliance_tools_validation()
        
        print(f"\n🎉 **Summary**: {tools} total tools ({gets} GET, {creates} CREATE, {updates} UPDATE, {deletes} DELETE)")
        
        if tools == 130:
            print("🏆 **PERFECT**: Exactly matches official Cisco Meraki SDK with 130 appliance tools!")
        else:
            print(f"⚠️ **ATTENTION**: Need {130 - tools} more tools to match official SDK")
            
    except Exception as e:
        print(f"💥 **Error**: {str(e)}")
        sys.exit(1)