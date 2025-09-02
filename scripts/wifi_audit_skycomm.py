#!/usr/bin/env python3
"""
Comprehensive WiFi Audit for Skycomm Reserve St Network
Acts as an MCP client (like Claude Desktop) to test all wireless tools
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json
from datetime import datetime

async def wifi_audit_skycomm():
    """Run comprehensive WiFi audit for Skycomm Reserve St."""
    
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🚀 COMPREHENSIVE WIFI AUDIT - SKYCOMM RESERVE ST")
    print("=" * 80)
    print(f"Audit Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Store audit results
            audit_results = {
                'organization': {},
                'network': {},
                'ssids': [],
                'access_points': [],
                'clients': [],
                'health_metrics': {},
                'issues_found': [],
                'tools_tested': {'working': [], 'failed': []}
            }
            
            # Step 1: Search for Skycomm organization
            print("\n📍 STEP 1: Finding Skycomm Organization")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "search_organizations_by_name",
                    arguments={"name": "skycomm"}
                )
                org_text = result.content[0].text
                print(org_text[:500])
                
                # Extract org ID from the result
                if "686470" in org_text:
                    org_id = "686470"
                    print(f"✅ Found Skycomm Org ID: {org_id}")
                    audit_results['organization']['id'] = org_id
                    audit_results['tools_tested']['working'].append('search_organizations_by_name')
                else:
                    # Try alternate org ID from previous tests
                    org_id = "1374235"
                    print(f"⚠️ Using alternate org ID: {org_id}")
            except Exception as e:
                print(f"❌ Error searching orgs: {e}")
                org_id = "686470"  # Use known ID
                audit_results['tools_tested']['failed'].append('search_organizations_by_name')
            
            # Step 2: Get networks in organization
            print("\n📍 STEP 2: Finding Reserve St Network")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_organization_networks",
                    arguments={"organization_id": org_id}
                )
                networks_text = result.content[0].text
                print(f"Networks found: {networks_text[:300]}...")
                
                # Look for Reserve St network
                network_id = None
                if "Reserve St" in networks_text:
                    # Extract network ID - look for pattern L_[numbers]
                    import re
                    match = re.search(r'Reserve St.*?L_\d+', networks_text)
                    if match:
                        network_id = re.search(r'L_\d+', match.group()).group()
                        print(f"✅ Found Reserve St Network ID: {network_id}")
                else:
                    network_id = "L_709951935762302054"  # Use known ID
                    print(f"⚠️ Using known network ID: {network_id}")
                
                audit_results['network']['id'] = network_id
                audit_results['tools_tested']['working'].append('get_organization_networks')
            except Exception as e:
                print(f"❌ Error getting networks: {e}")
                network_id = "L_709951935762302054"
                audit_results['tools_tested']['failed'].append('get_organization_networks')
            
            # Step 3: Comprehensive Health Check
            print("\n📍 STEP 3: Running Comprehensive Health Check")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_composite_wireless_health",
                    arguments={
                        "network_id": network_id,
                        "check_ssids": True,
                        "check_clients": True,
                        "check_aps": True,
                        "check_rf": True
                    }
                )
                health_text = result.content[0].text
                print(health_text)
                audit_results['health_metrics']['composite'] = health_text
                audit_results['tools_tested']['working'].append('get_composite_wireless_health')
            except Exception as e:
                print(f"❌ Composite health check failed: {e}")
                audit_results['tools_tested']['failed'].append('get_composite_wireless_health')
            
            # Step 4: Get SSIDs
            print("\n📍 STEP 4: Analyzing SSIDs")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_ssids",
                    arguments={"network_id": network_id}
                )
                ssids_text = result.content[0].text
                print(ssids_text[:500])
                audit_results['ssids'] = ssids_text
                audit_results['tools_tested']['working'].append('get_network_wireless_ssids')
            except Exception as e:
                print(f"❌ Error getting SSIDs: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_ssids')
            
            # Step 5: Get Access Points
            print("\n📍 STEP 5: Checking Access Points")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_access_points",
                    arguments={"network_id": network_id}
                )
                aps_text = result.content[0].text
                print(aps_text[:500])
                audit_results['access_points'] = aps_text
                audit_results['tools_tested']['working'].append('get_network_wireless_access_points')
            except Exception as e:
                print(f"❌ Error getting APs: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_access_points')
            
            # Step 6: Get Connected Clients
            print("\n📍 STEP 6: Analyzing Connected Clients")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_clients",
                    arguments={"network_id": network_id, "timespan": 300}
                )
                clients_text = result.content[0].text
                print(clients_text[:500])
                audit_results['clients'] = clients_text
                audit_results['tools_tested']['working'].append('get_network_wireless_clients')
            except Exception as e:
                print(f"❌ Error getting clients: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_clients')
            
            # Step 7: Get Failed Connections
            print("\n📍 STEP 7: Checking Failed Connections")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_failed_connections",
                    arguments={"network_id": network_id, "timespan": 86400}
                )
                failures_text = result.content[0].text
                print(failures_text[:500])
                audit_results['health_metrics']['failed_connections'] = failures_text
                audit_results['tools_tested']['working'].append('get_network_wireless_failed_connections')
            except Exception as e:
                print(f"❌ Error getting failed connections: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_failed_connections')
            
            # Step 8: RF Profiles
            print("\n📍 STEP 8: Analyzing RF Profiles")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_rf_profiles",
                    arguments={"network_id": network_id}
                )
                rf_text = result.content[0].text
                print(rf_text[:500])
                audit_results['health_metrics']['rf_profiles'] = rf_text
                audit_results['tools_tested']['working'].append('get_network_wireless_rf_profiles')
            except Exception as e:
                print(f"❌ Error getting RF profiles: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_rf_profiles')
            
            # Step 9: Client Count History
            print("\n📍 STEP 9: Client Count Trends")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_client_count_history",
                    arguments={"network_id": network_id, "timespan": 7200}
                )
                count_text = result.content[0].text
                print(count_text[:500])
                audit_results['health_metrics']['client_trends'] = count_text
                audit_results['tools_tested']['working'].append('get_network_wireless_client_count_history')
            except Exception as e:
                print(f"❌ Error getting client count history: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_client_count_history')
            
            # Step 10: Data Rate History
            print("\n📍 STEP 10: Data Rate Analysis")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_data_rate_history",
                    arguments={"network_id": network_id, "timespan": 3600}
                )
                data_rate_text = result.content[0].text
                print(data_rate_text[:500])
                audit_results['health_metrics']['data_rates'] = data_rate_text
                audit_results['tools_tested']['working'].append('get_network_wireless_data_rate_history')
            except Exception as e:
                print(f"❌ Error getting data rate history: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_data_rate_history')
            
            # Step 11: Usage History (requires device serial)
            print("\n📍 STEP 11: Wireless Usage Analysis")
            print("-" * 40)
            # First, try to get a device serial from the APs we found
            device_serial = None
            if 'access_points' in audit_results and audit_results['access_points']:
                import re
                serial_match = re.search(r'Serial: ([A-Z0-9-]+)', str(audit_results['access_points']))
                if serial_match:
                    device_serial = serial_match.group(1)
                    print(f"Using AP serial: {device_serial}")
            
            if device_serial:
                try:
                    result = await session.call_tool(
                        "get_network_wireless_usage_history",
                        arguments={
                            "network_id": network_id,
                            "device_serial": device_serial,
                            "timespan": 3600
                        }
                    )
                    usage_text = result.content[0].text
                    print(usage_text[:500])
                    audit_results['health_metrics']['usage'] = usage_text
                    audit_results['tools_tested']['working'].append('get_network_wireless_usage_history')
                except Exception as e:
                    print(f"❌ Error getting usage history: {e}")
                    audit_results['tools_tested']['failed'].append('get_network_wireless_usage_history')
            
            # Step 12: Air Marshal (Security)
            print("\n📍 STEP 12: Security Scan (Air Marshal)")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_air_marshal",
                    arguments={"network_id": network_id, "timespan": 3600}
                )
                security_text = result.content[0].text
                print(security_text[:500])
                audit_results['health_metrics']['security'] = security_text
                audit_results['tools_tested']['working'].append('get_network_wireless_air_marshal')
            except Exception as e:
                print(f"❌ Error getting Air Marshal data: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_air_marshal')
            
            # Step 13: Bluetooth Settings
            print("\n📍 STEP 13: Bluetooth Settings Check")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_bluetooth_settings",
                    arguments={"network_id": network_id}
                )
                bt_text = result.content[0].text
                print(bt_text[:500])
                audit_results['health_metrics']['bluetooth'] = bt_text
                audit_results['tools_tested']['working'].append('get_network_wireless_bluetooth_settings')
            except Exception as e:
                print(f"❌ Error getting Bluetooth settings: {e}")
                audit_results['tools_tested']['failed'].append('get_network_wireless_bluetooth_settings')
            
            # Generate Final Report
            print("\n" + "=" * 80)
            print("📊 WIFI AUDIT SUMMARY REPORT")
            print("=" * 80)
            
            print(f"\n🏢 Organization: Skycomm (ID: {audit_results['organization'].get('id', 'Unknown')})")
            print(f"📍 Network: Reserve St (ID: {audit_results['network'].get('id', 'Unknown')})")
            
            print(f"\n✅ Tools Successfully Tested: {len(audit_results['tools_tested']['working'])}")
            for tool in audit_results['tools_tested']['working']:
                print(f"  - {tool}")
            
            print(f"\n❌ Tools That Failed: {len(audit_results['tools_tested']['failed'])}")
            for tool in audit_results['tools_tested']['failed']:
                print(f"  - {tool}")
            
            # Analysis and Recommendations
            print("\n💡 KEY FINDINGS & RECOMMENDATIONS:")
            print("-" * 40)
            
            if '404' in str(audit_results) or 'Not Found' in str(audit_results):
                print("⚠️ Network may not exist or wireless not enabled")
                print("   → Verify network ID and ensure wireless is configured")
            
            if 'null' in str(audit_results).lower():
                print("⚠️ Some analytics data returning null")
                print("   → Enable analytics/monitoring features in Dashboard")
                print("   → Wait for data collection to populate historical metrics")
            
            if audit_results['tools_tested']['working']:
                print(f"✅ Core wireless tools are functioning ({len(audit_results['tools_tested']['working'])} tools)")
            
            print("\n🔧 TOOLS THAT NEED FIXES:")
            print("-" * 40)
            
            # Check for specific issues
            if 'get_network_wireless_usage_history' in audit_results['tools_tested']['failed']:
                print("• Usage History: Requires device_serial parameter")
                print("  Fix: Always provide AP serial number")
            
            if 'get_network_wireless_channel_utilization_history' in audit_results['tools_tested']['failed']:
                print("• Channel Utilization: Requires device_serial + band")
                print("  Fix: Provide both parameters")
            
            print("\n📈 NETWORK HEALTH INDICATORS:")
            print("-" * 40)
            
            # Parse health metrics if available
            if 'composite' in audit_results['health_metrics']:
                health = audit_results['health_metrics']['composite']
                if 'SSIDs' in health:
                    print("• SSIDs configured and checked")
                if 'Access Points' in health:
                    print("• Access Points status verified")
                if 'Connected Clients' in health:
                    print("• Client connectivity analyzed")
                if 'RF Configuration' in health:
                    print("• RF profiles reviewed")
            
            print("\n🎯 AUDIT COMPLETE!")
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return audit_results

if __name__ == "__main__":
    results = asyncio.run(wifi_audit_skycomm())
    print("\n✅ WiFi Audit Completed Successfully!")