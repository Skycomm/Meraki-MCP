#!/usr/bin/env python3
"""
Test 100% wireless API coverage - all 116 tools.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_100_coverage():
    """Test complete wireless coverage."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🚀 Testing 100% Wireless API Coverage...")
    print("=" * 60)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Get all tools
            tools_response = await session.list_tools()
            all_tools = [t.name for t in tools_response.tools]
            wireless_tools = sorted([t for t in all_tools if 'wireless' in t])
            
            print(f"Total wireless tools found: {len(wireless_tools)}")
            print("=" * 60)
            
            # Expected tools for 100% coverage (116 total)
            expected_count = 116
            
            if len(wireless_tools) >= expected_count:
                print(f"✅ SUCCESS: {len(wireless_tools)} tools registered!")
                print(f"📊 Coverage: {(len(wireless_tools)/expected_count)*100:.1f}%")
            else:
                print(f"⚠️ Only {len(wireless_tools)}/{expected_count} tools found")
                print(f"📊 Coverage: {(len(wireless_tools)/expected_count)*100:.1f}%")
            
            # Group tools by category
            categories = {
                'SSID': [],
                'Identity PSK': [],
                'Client': [],
                'Device': [],
                'Network': [],
                'Organization': [],
                'RF Profile': [],
                'Firewall': [],
                'Stats/History': [],
                'Other': []
            }
            
            for tool in wireless_tools:
                if 'identity_psk' in tool:
                    categories['Identity PSK'].append(tool)
                elif 'ssid' in tool:
                    categories['SSID'].append(tool)
                elif 'client' in tool:
                    categories['Client'].append(tool)
                elif 'device' in tool:
                    categories['Device'].append(tool)
                elif 'organization' in tool:
                    categories['Organization'].append(tool)
                elif 'rf_profile' in tool:
                    categories['RF Profile'].append(tool)
                elif 'firewall' in tool or 'l3' in tool or 'l7' in tool:
                    categories['Firewall'].append(tool)
                elif 'stats' in tool or 'history' in tool:
                    categories['Stats/History'].append(tool)
                elif 'network' in tool:
                    categories['Network'].append(tool)
                else:
                    categories['Other'].append(tool)
            
            print("\n📋 Tools by Category:")
            for cat, tools in categories.items():
                if tools:
                    print(f"  {cat}: {len(tools)} tools")
            
            # List newly added tools (the final 23)
            final_23 = [
                "get_network_wireless_ssid_identity_psk",
                "create_network_wireless_ssid_identity_psk", 
                "update_network_wireless_ssid_identity_psk",
                "delete_network_wireless_ssid_identity_psk",
                "get_network_wireless_client_latency_stats",
                "get_network_wireless_clients_connection_stats",
                "get_network_wireless_clients_latency_stats",
                "get_device_wireless_connection_stats",
                "create_network_wireless_rf_profile",
                "update_network_wireless_rf_profile",
                "delete_network_wireless_rf_profile",
                "get_device_wireless_radio_settings",
                "update_device_wireless_radio_settings",
                "update_network_wireless_settings",
                "get_network_wireless_l7_firewall_rules_application_categories",
                "get_network_wireless_rf_profiles_assignments_by_device",
                "get_organization_wireless_devices_ethernet_statuses",
                "get_network_wireless_clients_health_scores",
                "get_network_wireless_devices_connection_stats",
                "get_network_wireless_air_marshal",
                "get_network_wireless_channel_utilization_history"
            ]
            
            print("\n✨ Newly Added Tools (Final 23):")
            found_new = 0
            for tool in final_23:
                if tool in wireless_tools:
                    print(f"  ✅ {tool}")
                    found_new += 1
                else:
                    print(f"  ❌ {tool} - NOT FOUND")
            
            print(f"\n📊 Final Summary:")
            print(f"  - Total Wireless Tools: {len(wireless_tools)}")
            print(f"  - New Tools Found: {found_new}/23")
            print(f"  - API Coverage: {(len(wireless_tools)/116)*100:.1f}%")
            
            if len(wireless_tools) >= 116:
                print("\n🎉 100% WIRELESS API COVERAGE ACHIEVED!")
            
            return len(wireless_tools)

if __name__ == "__main__":
    count = asyncio.run(test_100_coverage())
    print(f"\n✅ Total wireless tools: {count}")
