#!/usr/bin/env python3
"""
Comprehensive test of ALL wireless tools in the MCP server.
Tests each tool and reports which ones work and which ones fail.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

# Test network and device IDs (from working networks)
TEST_ORG_ID = "686470"  # Skycomm org
TEST_NETWORK_ID = "L_709951935762302054"  # Reserve St network  
TEST_DEVICE_SERIAL = "Q2BV-K9A9-C3AZ"  # Example AP serial
TEST_CLIENT_ID = "k74272e"  # Example client ID
TEST_SSID_NUMBER = 0

async def test_all_wireless_tools():
    """Test all wireless tools and categorize them."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🚀 Testing ALL Wireless Tools")
    print("=" * 80)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get all tools
            tools_response = await session.list_tools()
            all_tools = [t.name for t in tools_response.tools]
            wireless_tools = sorted([t for t in all_tools if 'wireless' in t])
            
            print(f"Total wireless tools found: {len(wireless_tools)}")
            print("=" * 80)
            
            # Categories for results
            working_tools = []
            auth_failed = []
            not_found_404 = []
            missing_params = []
            null_data = []
            other_errors = []
            
            # Test each tool
            for i, tool_name in enumerate(wireless_tools, 1):
                print(f"\n[{i}/{len(wireless_tools)}] Testing: {tool_name}")
                print("-" * 40)
                
                # Prepare arguments based on tool name patterns
                args = {}
                
                # Network-based tools
                if 'network' in tool_name:
                    args['network_id'] = TEST_NETWORK_ID
                
                # Device-based tools  
                if 'device' in tool_name and 'network' not in tool_name:
                    args['serial'] = TEST_DEVICE_SERIAL
                elif 'device' in tool_name:
                    args['device_serial'] = TEST_DEVICE_SERIAL
                
                # Client-based tools
                if 'client' in tool_name and tool_name != 'get_network_wireless_client':
                    args['client_id'] = TEST_CLIENT_ID
                
                # SSID tools
                if 'ssid' in tool_name:
                    args['ssid_number'] = TEST_SSID_NUMBER
                    
                # Organization tools
                if 'organization' in tool_name:
                    args['organization_id'] = TEST_ORG_ID
                
                # Special cases
                if 'channel_utilization' in tool_name:
                    args['device_serial'] = TEST_DEVICE_SERIAL
                    args['band'] = '2.4'
                
                if 'usage_history' in tool_name or 'usage' in tool_name:
                    args['device_serial'] = TEST_DEVICE_SERIAL
                    
                if 'timespan' in tool_name or 'history' in tool_name:
                    args['timespan'] = 3600
                
                if 'signal_quality' in tool_name:
                    args['device_serial'] = TEST_DEVICE_SERIAL
                    
                # Try to call the tool
                try:
                    result = await session.call_tool(tool_name, arguments=args)
                    result_text = result.content[0].text if result.content else ""
                    
                    # Analyze result
                    if "401" in result_text or "Unauthorized" in result_text:
                        auth_failed.append(tool_name)
                        print("❌ 401 Unauthorized (API key issue)")
                    elif "404" in result_text or "Not Found" in result_text:
                        not_found_404.append(tool_name)
                        print("❌ 404 Not Found (network/device doesn't exist or no wireless)")
                    elif "Must specify" in result_text or "required" in result_text.lower():
                        missing_params.append(tool_name)
                        print(f"⚠️ Missing required parameters: {result_text[:100]}")
                    elif "null" in result_text.lower() or "None" in result_text:
                        null_data.append(tool_name)
                        print("⚠️ Returns NULL data (analytics not enabled or no data)")
                    elif "Error" in result_text or "error" in result_text:
                        other_errors.append((tool_name, result_text[:100]))
                        print(f"❌ Error: {result_text[:100]}")
                    else:
                        working_tools.append(tool_name)
                        print(f"✅ Working! Response length: {len(result_text)} chars")
                        if len(result_text) < 200:
                            print(f"   Response: {result_text}")
                            
                except Exception as e:
                    other_errors.append((tool_name, str(e)))
                    print(f"❌ Exception: {str(e)[:100]}")
            
            # Print summary
            print("\n" + "=" * 80)
            print("📊 SUMMARY REPORT")
            print("=" * 80)
            
            print(f"\n✅ WORKING TOOLS ({len(working_tools)}):")
            for tool in working_tools:
                print(f"  - {tool}")
                
            print(f"\n🔐 AUTH FAILED ({len(auth_failed)}):")
            for tool in auth_failed:
                print(f"  - {tool}")
                
            print(f"\n🔍 404 NOT FOUND ({len(not_found_404)}):")
            for tool in not_found_404:
                print(f"  - {tool}")
                
            print(f"\n⚠️ MISSING PARAMETERS ({len(missing_params)}):")
            for tool in missing_params:
                print(f"  - {tool}")
                
            print(f"\n📉 NULL/NO DATA ({len(null_data)}):")
            for tool in null_data:
                print(f"  - {tool}")
                
            print(f"\n❌ OTHER ERRORS ({len(other_errors)}):")
            for tool, error in other_errors:
                print(f"  - {tool}: {error}")
            
            print(f"\n📈 STATISTICS:")
            print(f"  Total Tools: {len(wireless_tools)}")
            print(f"  Working: {len(working_tools)} ({len(working_tools)*100//len(wireless_tools)}%)")
            print(f"  Auth Issues: {len(auth_failed)}")
            print(f"  Not Found: {len(not_found_404)}")
            print(f"  Missing Params: {len(missing_params)}")
            print(f"  No Data: {len(null_data)}")
            print(f"  Other Errors: {len(other_errors)}")
            
            # Recommendations
            print("\n💡 RECOMMENDATIONS:")
            if auth_failed:
                print("  - Check API key permissions for these endpoints")
            if not_found_404:
                print("  - These tools need a valid network with wireless enabled")
            if missing_params:
                print("  - These tools need specific parameters (device_serial, client_id, etc.)")
            if null_data:
                print("  - Enable analytics/monitoring on the network for these tools")
                
            return {
                'total': len(wireless_tools),
                'working': len(working_tools),
                'auth_failed': len(auth_failed),
                'not_found': len(not_found_404),
                'missing_params': len(missing_params),
                'null_data': len(null_data),
                'other_errors': len(other_errors)
            }

if __name__ == "__main__":
    results = asyncio.run(test_all_wireless_tools())
    print(f"\n🎯 Final Score: {results['working']}/{results['total']} tools working")
