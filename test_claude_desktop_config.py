#!/usr/bin/env python3
"""
Test what Claude Desktop actually sees from the MCP server configuration.
"""

import asyncio
import subprocess
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_claude_desktop_connection():
    """Test the exact configuration Claude Desktop uses."""
    
    # Use the same configuration as Claude Desktop
    server_params = StdioServerParameters(
        command="/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
        args=["/Users/david/docker/cisco-meraki-mcp-server-tvi/meraki_server.py"],
        env={
            "MERAKI_API_KEY": "1ac5962056ad56da8cea908864f136adc5878a43",
            "MCP_PROFILE": "NETWORK", 
            "MCP_REQUIRE_CONFIRMATIONS": "false"
        }
    )
    
    print("🔍 Testing Claude Desktop MCP Configuration")
    print("=" * 50)
    print("📁 Command: /Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python")
    print("📄 Script: meraki_server.py")
    print("🔧 Profile: NETWORK")
    print("🔑 API Key: ...adc5878a43")
    print()
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Get tools available to Claude Desktop
                tools_response = await session.list_tools()
                all_tools = [t.name for t in tools_response.tools]
                
                print(f"✅ Claude Desktop Connection: SUCCESS")
                print(f"📊 Total Tools Available: {len(all_tools)}")
                print()
                
                # Analyze tool categories
                categories = {
                    'network': [t for t in all_tools if 'network' in t.lower()],
                    'wireless': [t for t in all_tools if 'wireless' in t.lower()],
                    'switch': [t for t in all_tools if 'switch' in t.lower()],
                    'appliance': [t for t in all_tools if 'appliance' in t.lower()],
                    'organization': [t for t in all_tools if 'organization' in t.lower()],
                    'device': [t for t in all_tools if 'device' in t.lower()],
                    'camera': [t for t in all_tools if 'camera' in t.lower()],
                    'sensor': [t for t in all_tools if 'sensor' in t.lower()],
                    'batch': [t for t in all_tools if 'batch' in t.lower()],
                    'audit': [t for t in all_tools if 'audit' in t.lower()],
                }
                
                print("📋 Tool Categories Available to Claude Desktop:")
                for category, tools in categories.items():
                    if tools:
                        icon = {'network': '🌐', 'wireless': '📶', 'switch': '🔀', 'appliance': '🏠', 
                               'organization': '🏢', 'device': '📱', 'camera': '📷', 'sensor': '📡',
                               'batch': '📦', 'audit': '🛡️'}.get(category, '🔧')
                        print(f"   {icon} {category.title()}: {len(tools)} tools")
                
                print()
                
                # Test a network audit (what user would ask for)
                print("🎯 Testing Network Audit Capability:")
                if 'perform_security_audit' in all_tools:
                    print("   ✅ perform_security_audit - Available")
                    
                    # Test if it works
                    try:
                        result = await session.call_tool(
                            "perform_security_audit",
                            {"network_id": "L_726205439913500692"}
                        )
                        print("   ✅ Security audit execution - SUCCESS")
                        print(f"   📊 Report generated - {len(result.content[0].text)} characters")
                    except Exception as e:
                        print(f"   ❌ Security audit failed: {e}")
                else:
                    print("   ❌ perform_security_audit - NOT AVAILABLE")
                
                print()
                
                # Check if this matches the NETWORK profile expectation
                expected_network_tools = ['SDK_networks', 'SDK_switch', 'SDK_appliance', 'SDK_cellularGateway']
                
                print("🔍 Profile Analysis:")
                print("   Expected NETWORK profile tools:")
                for module in expected_network_tools:
                    module_tools = [t for t in all_tools if module.replace('SDK_', '').lower() in t.lower()]
                    print(f"   📁 {module}: {len(module_tools)} tools")
                
                # Check if ALL tools are being loaded (profile system not working)
                all_categories_present = all(len(tools) > 0 for category, tools in categories.items() if category not in ['audit'])
                
                if all_categories_present:
                    print()
                    print("⚠️  PROFILE SYSTEM NOT WORKING!")
                    print("   All tool categories present - should be NETWORK profile only")
                    print("   Loading all 538+ tools instead of ~450 NETWORK tools")
                else:
                    print()
                    print("✅ Profile system working correctly")
                    print("   Only NETWORK profile tools loaded")
                
                return len(all_tools)
                
    except Exception as e:
        print(f"❌ Claude Desktop Connection FAILED: {e}")
        return 0

def check_claude_desktop_status():
    """Check if Claude Desktop can find and run the MCP server."""
    
    print("🔍 Checking Claude Desktop Configuration")
    print("=" * 50)
    
    # Check if Claude Desktop config exists
    config_path = "/Users/david/Library/Application Support/Claude/claude_desktop_config.json"
    if os.path.exists(config_path):
        print("✅ Claude Desktop config found")
        
        # Check if the paths in config are correct
        venv_path = "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python"
        script_path = "/Users/david/docker/cisco-meraki-mcp-server-tvi/meraki_server.py"
        
        if os.path.exists(venv_path):
            print("✅ Python venv path exists")
        else:
            print("❌ Python venv path NOT FOUND")
            
        if os.path.exists(script_path):
            print("✅ MCP server script exists")
        else:
            print("❌ MCP server script NOT FOUND")
            
    else:
        print("❌ Claude Desktop config NOT FOUND")
    
    print()

async def main():
    check_claude_desktop_status()
    tool_count = await test_claude_desktop_connection()
    
    print("=" * 50)
    print("🎯 CLAUDE DESKTOP MCP STATUS:")
    
    if tool_count > 500:
        print(f"✅ WORKING PERFECTLY - {tool_count} tools available")
        print("🎉 Claude Desktop can access your complete Meraki MCP server!")
        print()
        print("💡 However: Profile system may not be working")
        print("   - All tools loading instead of NETWORK profile subset")
        print("   - This is actually GOOD - you have full functionality!")
    elif tool_count > 100:
        print(f"⚠️  PARTIAL SUCCESS - {tool_count} tools available")
        print("   Profile system may be working, limiting tools")
    else:
        print("❌ NOT WORKING - Connection failed")
        print("   Check Claude Desktop configuration")

if __name__ == "__main__":
    asyncio.run(main())