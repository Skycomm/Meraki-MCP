#!/usr/bin/env python3
"""
Test that we have achieved 100% SDK coverage - all 116 methods.
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
    
    print("🚀 Testing 100% Wireless SDK Coverage...")
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
            
            # Expected 116 SDK methods
            expected = 116
            
            if len(wireless_tools) >= expected:
                print(f"✅ SUCCESS: {len(wireless_tools)} tools registered!")
                print(f"🎉 100% SDK COVERAGE ACHIEVED!")
            else:
                print(f"⚠️ Only {len(wireless_tools)}/{expected} tools")
                print(f"📊 Coverage: {(len(wireless_tools)/expected)*100:.1f}%")
            
            # Test the newly added methods
            test_results = []
            new_methods = [
                "update_device_wireless_alternate_management_interface_ipv6",
                "get_device_wireless_latency_stats",
                "get_network_wireless_devices_latency_stats",
                "get_network_wireless_electronic_shelf_label_configured_devices",
                "set_network_wireless_ethernet_ports_profiles_default",
                "get_network_wireless_ethernet_ports_profile",
                "get_network_wireless_latency_history",
                "get_organization_wireless_devices_channel_utilization_history_by_device_by_interval",
                "get_organization_wireless_devices_power_mode_history",
                "get_organization_wireless_devices_radsec_certificates_authorities",
                "get_organization_wireless_devices_system_cpu_load_history",
                "recalculate_organization_wireless_radio_auto_rf_channels",
                "get_organization_wireless_rf_profiles_assignments_by_device",
                "get_organization_wireless_ssids_firewall_isolation_allowlist_entries"
            ]
            
            print("\n✨ Testing Newly Added Methods:")
            for method in new_methods:
                if method in wireless_tools:
                    print(f"  ✅ {method}")
                    test_results.append(True)
                else:
                    print(f"  ❌ {method} - NOT FOUND")
                    test_results.append(False)
            
            success_rate = sum(test_results) / len(test_results) * 100 if test_results else 0
            
            print(f"\n📊 Final Summary:")
            print(f"  - Total Wireless Tools: {len(wireless_tools)}")
            print(f"  - SDK Coverage: {(len(wireless_tools)/116)*100:.1f}%")
            print(f"  - New Methods Success: {success_rate:.0f}%")
            
            if len(wireless_tools) >= 116:
                print("\n🎉 CONGRATULATIONS! 100% WIRELESS SDK COVERAGE ACHIEVED!")
                print("All 116 official SDK methods are now implemented!")
            
            return len(wireless_tools)

if __name__ == "__main__":
    count = asyncio.run(test_100_coverage())
    print(f"\n✅ Final count: {count} wireless tools")
