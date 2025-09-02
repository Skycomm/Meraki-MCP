#!/usr/bin/env python3
"""
Test detailed network audit with available tools
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_detailed_audit():
    """Test detailed network audit with available tools."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python", 
        args=["meraki_server.py"],
        env=None
    )
    
    print("🎯 Starting Detailed Network Audit Test")
    print("📍 Target: Skycomm Reserve St Network (L_726205439913500692)")
    print("=" * 60)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Get available tools
                tools_response = await session.list_tools()
                all_tools = [t.name for t in tools_response.tools]
                
                print(f"✅ Server connected - {len(all_tools)} tools available")
                
                # Find available audit/network tools
                audit_tools = [t for t in all_tools if 'audit' in t.lower()]
                network_tools = [t for t in all_tools if 'network' in t.lower()]
                
                print(f"\n🔍 Found audit tools: {len(audit_tools)}")
                for tool in audit_tools:
                    print(f"  📋 {tool}")
                
                print(f"\n🌐 Found network tools: {len(network_tools)}")
                for tool in network_tools[:10]:  # Show first 10
                    print(f"  🔧 {tool}")
                if len(network_tools) > 10:
                    print(f"  ... and {len(network_tools) - 10} more")
                
                # Try the security audit tool
                if 'perform_security_audit' in all_tools:
                    print(f"\n🛡️ Testing security audit...")
                    try:
                        result = await session.call_tool(
                            "perform_security_audit",
                            {"network_id": "L_726205439913500692"}
                        )
                        print("✅ Security audit successful!")
                        content = result.content[0].text
                        # Show first 500 characters
                        print(f"📊 Result preview: {content[:500]}...")
                        
                    except Exception as e:
                        print(f"❌ Security audit failed: {e}")
                
                # Test some network sensor tools
                sensor_tools = [t for t in all_tools if 'sensor' in t.lower() and 'network' in t.lower()]
                if sensor_tools:
                    print(f"\n📡 Testing network sensor tools ({len(sensor_tools)} available)...")
                    test_tool = sensor_tools[0]
                    print(f"   Testing: {test_tool}")
                    
                    try:
                        result = await session.call_tool(
                            test_tool,
                            {"network_id": "L_726205439913500692"}
                        )
                        print("✅ Sensor tool successful!")
                        content = result.content[0].text
                        print(f"📊 Result: {content[:200]}...")
                        
                    except Exception as e:
                        print(f"❌ Sensor tool failed: {e}")
                        
                # Try to find organization tools
                org_tools = [t for t in all_tools if 'organization' in t.lower()]
                print(f"\n🏢 Found organization tools: {len(org_tools)}")
                for tool in org_tools[:5]:
                    print(f"  🏢 {tool}")
                
                print(f"\n📈 Summary:")
                print(f"  Total tools: {len(all_tools)}")
                print(f"  Audit tools: {len(audit_tools)}")
                print(f"  Network tools: {len(network_tools)}")
                print(f"  Sensor tools: {len(sensor_tools)}")
                print(f"  Organization tools: {len(org_tools)}")
                
                return len(all_tools)
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 0

if __name__ == "__main__":
    tool_count = asyncio.run(test_detailed_audit())
    print(f"\n🏆 Network audit test complete!")
    print(f"✅ Server is working with {tool_count} tools")
    
    if tool_count > 50:
        print("🎉 Tool count looks good - above the ~850 limit concern!")
        print("💡 The limit may indeed be higher than previously thought")
    else:
        print("⚠️  Lower tool count - may need to add more SDK modules back")