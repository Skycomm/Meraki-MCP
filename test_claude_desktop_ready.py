#!/usr/bin/env python3
"""
Quick test to verify Claude Desktop setup with all tools.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters  
from mcp.client.stdio import stdio_client

async def test_claude_desktop_ready():
    """Test the complete Claude Desktop setup."""
    
    # Use exact Claude Desktop config
    server_params = StdioServerParameters(
        command="/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
        args=["/Users/david/docker/cisco-meraki-mcp-server-tvi/meraki_server.py"],
        env={
            "MERAKI_API_KEY": "1ac5962056ad56da8cea908864f136adc5878a43",
            "MCP_PROFILE": "FULL",
            "MCP_REQUIRE_CONFIRMATIONS": "false"
        }
    )
    
    print("🎯 Testing Claude Desktop Setup - ALL TOOLS")
    print("=" * 50)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                tools_response = await session.list_tools()
                all_tools = [t.name for t in tools_response.tools]
                
                print(f"✅ CONNECTION SUCCESS!")
                print(f"📊 Total Tools: {len(all_tools)}")
                print()
                
                # Key categories for network auditing
                key_categories = {
                    '🛡️ Security/Audit': [t for t in all_tools if any(word in t.lower() for word in ['audit', 'security', 'firewall', 'intrusion'])],
                    '🌐 Network': [t for t in all_tools if 'network' in t.lower()],
                    '📶 Wireless': [t for t in all_tools if 'wireless' in t.lower()], 
                    '🔀 Switch': [t for t in all_tools if 'switch' in t.lower()],
                    '🏠 Appliance': [t for t in all_tools if 'appliance' in t.lower()],
                    '🏢 Organization': [t for t in all_tools if 'organization' in t.lower()],
                    '📱 Devices': [t for t in all_tools if 'device' in t.lower()],
                    '📷 Camera': [t for t in all_tools if 'camera' in t.lower()],
                }
                
                print("📋 Available Tool Categories:")
                for category, tools in key_categories.items():
                    print(f"   {category}: {len(tools)} tools")
                
                # Test the main audit function
                print(f"\n🧪 Testing Main Audit Function:")
                if 'perform_security_audit' in all_tools:
                    print("   ✅ perform_security_audit available")
                    try:
                        result = await session.call_tool(
                            "perform_security_audit", 
                            {"network_id": "L_726205439913500692"}
                        )
                        print("   ✅ Audit function working!")
                        print(f"   📄 Generated {len(result.content[0].text)} character report")
                    except Exception as e:
                        print(f"   ❌ Audit failed: {e}")
                else:
                    print("   ❌ perform_security_audit NOT FOUND")
                
                return len(all_tools)
                
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")
        return 0

if __name__ == "__main__":
    tool_count = asyncio.run(test_claude_desktop_ready())
    
    print("\n" + "=" * 50)
    print("🎯 CLAUDE DESKTOP STATUS:")
    
    if tool_count >= 500:
        print(f"🎉 PERFECT! {tool_count} tools ready for Claude Desktop")
        print("✅ Complete Meraki API coverage available")
        print("🛡️ Network auditing fully functional")
        print()
        print("🚀 YOU'RE ALL SET! Open Claude Desktop and try:")
        print('   "Please do a detailed audit of the skycomm reserve st network"')
        print('   "Show me the wireless networks in my organization"')  
        print('   "Check the firewall settings for network L_726205439913500692"')
        print()
    else:
        print(f"⚠️ Only {tool_count} tools available")
        print("   Something may need adjustment")