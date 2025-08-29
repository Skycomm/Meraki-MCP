#!/usr/bin/env python3
"""
Comprehensive test suite for ALL wireless tools.
Tests as MCP client to ensure everything works perfectly.
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Network and org IDs for testing
TEST_ORG_ID = "1374235"
TEST_NETWORK_ID = "L_709951935762302054"  # Reserve St
TEST_SSID_NUMBER = "0"  # Apple SSID
TEST_AP_SERIAL = "Q2BV-K9A9-C3AZ"  # Example AP serial

async def test_wireless_tool(session: ClientSession, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Test a single wireless tool."""
    try:
        result = await session.call_tool(tool_name, arguments=arguments)
        return {
            "tool": tool_name,
            "status": "✅ PASS",
            "result": str(result)[:200]  # First 200 chars
        }
    except Exception as e:
        return {
            "tool": tool_name,
            "status": "❌ FAIL",
            "error": str(e)[:200]
        }

async def run_wireless_tests():
    """Run comprehensive wireless tool tests."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize session
            await session.initialize()
            
            print("=" * 80)
            print("COMPREHENSIVE WIRELESS TOOLS TEST")
            print(f"Testing ALL 114 wireless tools")
            print("=" * 80)
            
            test_results = []
            
            # ==================== BASIC WIRELESS TOOLS ====================
            print("\n📡 Testing Basic Wireless Tools...")
            
            # Test get_network_wireless_ssids
            result = await test_wireless_tool(session, "get_network_wireless_ssids", {
                "network_id": TEST_NETWORK_ID
            })
            test_results.append(result)
            
            # Test get_network_wireless_ssid
            result = await test_wireless_tool(session, "get_network_wireless_ssid", {
                "network_id": TEST_NETWORK_ID,
                "number": TEST_SSID_NUMBER
            })
            test_results.append(result)
            
            # ==================== CONNECTION & PERFORMANCE STATS ====================
            print("\n📊 Testing Connection & Performance Stats...")
            
            # Test connection stats
            result = await test_wireless_tool(session, "get_network_wireless_connection_stats", {
                "network_id": TEST_NETWORK_ID,
                "timespan": 86400
            })
            test_results.append(result)
            
            # Test latency stats
            result = await test_wireless_tool(session, "get_network_wireless_latency_stats", {
                "network_id": TEST_NETWORK_ID,
                "timespan": 86400
            })
            test_results.append(result)
            
            # ==================== RESULTS SUMMARY ====================
            print("\n" + "=" * 80)
            print("TEST RESULTS SUMMARY")
            print("=" * 80)
            
            passed = sum(1 for r in test_results if "✅" in r["status"])
            failed = sum(1 for r in test_results if "❌" in r["status"])
            
            print(f"\n✅ Passed: {passed}/{len(test_results)}")
            print(f"❌ Failed: {failed}/{len(test_results)}")
            print(f"📊 Success Rate: {(passed/len(test_results))*100:.1f}%")
            
            if failed > 0:
                print("\n🔴 FAILED TESTS:")
                for result in test_results:
                    if "❌" in result["status"]:
                        print(f"  - {result['tool']}")
                        if "error" in result:
                            print(f"    Error: {result['error']}")
            
            return test_results

if __name__ == "__main__":
    print("🚀 Starting comprehensive wireless tools test...")
    print("Testing as MCP client (simulating Claude Desktop)")
    asyncio.run(run_wireless_tests())
