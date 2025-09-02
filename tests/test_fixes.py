#!/usr/bin/env python3
"""Test the fixes made to wireless tools."""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_fixes():
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🧪 Testing Fixes for Wireless Tools")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            network_id = "L_726205439913500692"  # Reserve St
            
            # Test 1: AP Status Fix
            print("\n1️⃣ Testing AP Status Display Fix:")
            try:
                result = await session.call_tool(
                    "get_network_wireless_access_points",
                    arguments={"network_id": network_id}
                )
                text = result.content[0].text
                print(text[:400])
                if "✅" in text or "❌" in text or "⚠️" in text:
                    print("✅ AP status icons working!")
                else:
                    print("⚠️ AP status may still need work")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 2: Composite Health with Better Status
            print("\n2️⃣ Testing Composite Health Status Fix:")
            try:
                result = await session.call_tool(
                    "get_composite_wireless_health",
                    arguments={
                        "network_id": network_id,
                        "check_aps": True
                    }
                )
                text = result.content[0].text
                if "Unknown Status" in text or "IP:" in text:
                    print("✅ Better AP status detection working!")
                else:
                    print("⚠️ May need more work")
                print(text[:400])
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 3: Analytics null data handling
            print("\n3️⃣ Testing Analytics Null Data Handling:")
            try:
                result = await session.call_tool(
                    "get_network_wireless_client_count_history",
                    arguments={"network_id": network_id, "timespan": 3600}
                )
                text = result.content[0].text
                if "No data available" in text or "Analytics data collection" in text:
                    print("✅ Null data handling improved!")
                print(text[:400])
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("\n✅ Tests Complete!")

if __name__ == "__main__":
    asyncio.run(test_fixes())
