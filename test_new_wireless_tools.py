#!/usr/bin/env python3
"""
Test newly added wireless tools to ensure they work correctly.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

TEST_NETWORK_ID = "L_709951935762302054"  # Reserve St
TEST_SSID_NUMBER = "0"  # Apple SSID
TEST_ORG_ID = "1374235"

async def test_tools():
    """Test new wireless tools."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 60)
            print("TESTING NEW WIRELESS TOOLS")
            print("=" * 60)
            
            tests = [
                # Connection stats
                ("get_network_wireless_connection_stats", {
                    "network_id": TEST_NETWORK_ID,
                    "timespan": 86400
                }),
                # Splash settings
                ("get_network_wireless_ssid_splash_settings", {
                    "network_id": TEST_NETWORK_ID,
                    "number": TEST_SSID_NUMBER
                }),
                # Hotspot 2.0
                ("get_network_wireless_ssid_hotspot20", {
                    "network_id": TEST_NETWORK_ID,
                    "number": TEST_SSID_NUMBER
                }),
                # Wireless settings
                ("get_network_wireless_settings", {
                    "network_id": TEST_NETWORK_ID
                }),
                # Bluetooth settings
                ("get_network_wireless_bluetooth_settings", {
                    "network_id": TEST_NETWORK_ID
                })
            ]
            
            passed = 0
            failed = 0
            
            for tool_name, args in tests:
                try:
                    print(f"\nTesting {tool_name}...", end=" ")
                    result = await session.call_tool(tool_name, arguments=args)
                    print("✅ PASS")
                    passed += 1
                except Exception as e:
                    print(f"❌ FAIL: {str(e)[:50]}")
                    failed += 1
            
            print("\n" + "=" * 60)
            print(f"Results: {passed} passed, {failed} failed")
            print("=" * 60)
            
            return passed, failed

if __name__ == "__main__":
    passed, failed = asyncio.run(test_tools())
    if failed == 0:
        print("\n🎉 All new wireless tools working perfectly!")
    else:
        print(f"\n⚠️ {failed} tools need attention")
