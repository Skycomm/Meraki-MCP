#!/usr/bin/env python3
"""
Test MCP client with a detailed network audit request.
This will show us actual tool counts and any limit issues.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

async def test_network_audit():
    """Test detailed network audit with MCP client."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🚀 Starting MCP Client Test...")
    print("🎯 Request: Detailed audit of Skycomm Reserve St network")
    print("=" * 60)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Get all available tools first
                print("📊 Getting available tools...")
                tools_response = await session.list_tools()
                all_tools = [t.name for t in tools_response.tools]
                
                print(f"✅ Total tools available: {len(all_tools)}")
                print(f"   SDK tools: {len([t for t in all_tools if 'SDK' in t or any(cat in t for cat in ['network', 'device', 'wireless', 'switch', 'appliance', 'organization'])])}")
                print(f"   Custom tools: {len([t for t in all_tools if 'custom' in t.lower() or 'helper' in t.lower()])}")
                
                # Look for network-related tools
                network_tools = [t for t in all_tools if 'network' in t.lower()]
                wireless_tools = [t for t in all_tools if 'wireless' in t.lower()]
                device_tools = [t for t in all_tools if 'device' in t.lower()]
                switch_tools = [t for t in all_tools if 'switch' in t.lower()]
                
                print(f"\n🔍 Relevant tool categories:")
                print(f"   Network tools: {len(network_tools)}")
                print(f"   Wireless tools: {len(wireless_tools)}")  
                print(f"   Device tools: {len(device_tools)}")
                print(f"   Switch tools: {len(switch_tools)}")
                
                # Test the audit request
                print(f"\n🎯 Testing network audit request...")
                
                # Use the call_tool method to make the request
                audit_request = """
                Please do a detailed audit of the Skycomm Reserve St network. 
                I want to understand:
                1. Network overview and configuration
                2. All devices and their status
                3. Wireless network health and performance  
                4. Switch configurations and connectivity
                5. Any issues or recommendations
                
                Use the test network ID: L_726205439913500692
                """
                
                # Call a simple tool first to test
                try:
                    result = await session.call_tool(
                        "get_network",
                        {"network_id": "L_726205439913500692"}
                    )
                    print("✅ Basic network call successful")
                    print(f"   Result: {result.content[0].text[:200]}...")
                    
                except Exception as e:
                    print(f"❌ Tool call failed: {e}")
                    
                    # Check if it's a tool limit issue
                    if "limit" in str(e).lower() or "too many" in str(e).lower():
                        print("🚨 TOOL LIMIT HIT!")
                        print("   This confirms we're still registering too many tools")
                    
                # Try to find specific audit or helper tools
                audit_tools = [t for t in all_tools if 'audit' in t.lower()]
                helper_tools = [t for t in all_tools if 'helper' in t.lower()]
                
                print(f"\n🔧 Utility tools available:")
                print(f"   Audit tools: {len(audit_tools)} - {audit_tools[:3]}")
                print(f"   Helper tools: {len(helper_tools)} - {helper_tools[:3]}")
                
                # Show some example network tools
                print(f"\n📋 Sample network tools (first 10):")
                for i, tool in enumerate(network_tools[:10]):
                    print(f"   {i+1}. {tool}")
                
                return len(all_tools)
                
    except Exception as e:
        print(f"❌ MCP Client Error: {e}")
        
        # Check if it's related to too many tools
        if "limit" in str(e).lower() or "register" in str(e).lower():
            print("🚨 POSSIBLE TOOL REGISTRATION ISSUE!")
            print("   Server may be registering duplicate tools from multiple files")
        
        return 0

def check_duplicate_registrations():
    """Check for potential duplicate tool registrations."""
    
    print("\n🔍 Checking for duplicate registrations...")
    print("=" * 50)
    
    # Check main.py for what's being imported and called
    with open('server/main.py', 'r') as f:
        main_content = f.read()
    
    # Count register_ function calls
    register_calls = []
    for line in main_content.split('\n'):
        if 'register_' in line and '(' in line and not line.strip().startswith('#'):
            register_calls.append(line.strip())
    
    print(f"📊 Registration calls in main.py: {len(register_calls)}")
    for call in register_calls:
        print(f"   {call}")
    
    # Check if there are any old tool files still being imported
    old_tool_files = [
        'server/tools_networks.py',
        'server/tools_wireless.py', 
        'server/tools_organizations.py',
        'server/tools_appliance.py'
    ]
    
    print(f"\n🔍 Checking for old tool files...")
    import os
    for old_file in old_tool_files:
        if os.path.exists(old_file):
            print(f"⚠️  Found old file: {old_file}")
            with open(old_file, 'r') as f:
                content = f.read()
                tool_count = content.count('@app.tool')
            print(f"   Contains {tool_count} tools - may cause duplicates!")
        else:
            print(f"✅ {old_file} - removed")

if __name__ == "__main__":
    print("🧪 Testing MCP Tool Limits and Registrations")
    print("=" * 60)
    
    # Check for duplicates first
    check_duplicate_registrations()
    
    # Test with MCP client
    tool_count = asyncio.run(test_network_audit())
    
    print(f"\n📈 Final Results:")
    print(f"   Total tools registered: {tool_count}")
    print(f"   Expected SDK tools: 816")
    print(f"   Expected custom tools: ~74")
    print(f"   Expected total: ~890")
    
    if tool_count > 900:
        print("⚠️  Tool count higher than expected - likely duplicates!")
    elif tool_count == 0:
        print("❌ Server failed to start - check for import/registration errors")
    else:
        print("✅ Tool count within expected range")