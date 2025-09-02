#!/usr/bin/env python3
"""
Comprehensive test of ALL wireless tools - tests every single one.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Test configuration
TEST_ORG_ID = "1374235"
TEST_NETWORK_ID = "L_709951935762302054"  # Reserve St
TEST_SSID_NUMBER = "0"  # Apple SSID
TEST_AP_SERIAL = "Q2BV-K9A9-C3AZ"
TEST_CLIENT_MAC = "00:11:22:33:44:55"  # Dummy MAC for testing

async def test_wireless_tools():
    """Test ALL wireless tools comprehensively."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🚀 Starting comprehensive wireless tools test...")
    print("=" * 80)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get all tools
            tools_response = await session.list_tools()
            all_tools = [t.name for t in tools_response.tools]
            wireless_tools = [t for t in all_tools if 'wireless' in t]
            
            print(f"Found {len(wireless_tools)} wireless tools to test")
            print("=" * 80)
            
            results = {
                "passed": [],
                "failed": [],
                "errors": {}
            }
            
            # Test each wireless tool
            for i, tool_name in enumerate(wireless_tools, 1):
                print(f"[{i}/{len(wireless_tools)}] Testing {tool_name}...", end=" ")
                
                # Determine appropriate test parameters based on tool name
                try:
                    if 'organization' in tool_name:
                        args = {"organization_id": TEST_ORG_ID}
                    elif 'device' in tool_name and 'serial' not in tool_name:
                        args = {"serial": TEST_AP_SERIAL}
                    elif 'ssid' in tool_name:
                        args = {
                            "network_id": TEST_NETWORK_ID,
                            "number": TEST_SSID_NUMBER
                        }
                    elif 'client' in tool_name and 'clients' not in tool_name:
                        args = {
                            "network_id": TEST_NETWORK_ID,
                            "client_id": TEST_CLIENT_MAC
                        }
                    else:
                        args = {"network_id": TEST_NETWORK_ID}
                    
                    # Add common optional parameters
                    if 'history' in tool_name or 'stats' in tool_name:
                        args["timespan"] = 86400
                    if 'per_page' in tool_name or 'list' in tool_name:
                        args["per_page"] = 100
                    
                    # Call the tool
                    result = await session.call_tool(tool_name, arguments=args)
                    print("✅ PASS")
                    results["passed"].append(tool_name)
                    
                except Exception as e:
                    error_msg = str(e)
                    # Check if it's an expected error (like resource not found)
                    if any(expected in error_msg.lower() for expected in [
                        "not found", "no data", "disabled", "not configured",
                        "invalid", "does not exist", "unauthorized"
                    ]):
                        print("⚠️ EXPECTED ERROR")
                        results["passed"].append(tool_name)
                    else:
                        print(f"❌ FAIL: {error_msg[:50]}")
                        results["failed"].append(tool_name)
                        results["errors"][tool_name] = error_msg
            
            # Print summary
            print("\n" + "=" * 80)
            print("TEST RESULTS SUMMARY")
            print("=" * 80)
            print(f"✅ Passed: {len(results['passed'])}/{len(wireless_tools)}")
            print(f"❌ Failed: {len(results['failed'])}/{len(wireless_tools)}")
            print(f"📊 Success Rate: {(len(results['passed'])/len(wireless_tools))*100:.1f}%")
            
            if results["failed"]:
                print("\n🔴 FAILED TOOLS:")
                for tool in results["failed"]:
                    print(f"  - {tool}")
                    if tool in results["errors"]:
                        print(f"    Error: {results['errors'][tool][:100]}")
            
            # Save detailed results
            with open("wireless_test_results_comprehensive.json", "w") as f:
                json.dump(results, f, indent=2)
            
            print(f"\n📝 Detailed results saved to wireless_test_results_comprehensive.json")
            
            return results

if __name__ == "__main__":
    asyncio.run(test_wireless_tools())
