#!/usr/bin/env python3
"""
Test comprehensive WiFi audit for Skycomm Reserve St network.
This tests the exact scenario from the transcript with fixes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import traceback
from server.main import app, meraki

def test_wifi_audit():
    """
    Perform comprehensive WiFi audit using correct tool names and parameters.
    """
    print("🚀 Starting Comprehensive WiFi Audit for Skycomm Reserve St")
    print("=" * 70)
    
    # Test configuration
    org_id = "686470"
    network_id = "L_726205439913500692"
    results = {
        "successful": [],
        "failed": []
    }
    
    # Track which tools work
    print("\n📊 Testing WiFi Audit Tools...")
    print("-" * 70)
    
    # 1. Get Organizations
    try:
        print("\n1. Testing get_organizations...")
        orgs = meraki.dashboard.organizations.getOrganizations()
        print(f"   ✅ Found {len(orgs)} organizations")
        results["successful"].append("get_organizations")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_organizations", str(e)))
    
    # 2. Get Organization Networks
    try:
        print("\n2. Testing get_organization_networks...")
        networks = meraki.dashboard.organizations.getOrganizationNetworks(
            org_id, perPage=1000, total_pages='all'
        )
        print(f"   ✅ Found {len(networks)} networks")
        results["successful"].append("get_organization_networks")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_organization_networks", str(e)))
    
    # 3. Get Network Wireless SSIDs
    try:
        print("\n3. Testing get_network_wireless_ssids...")
        ssids = meraki.dashboard.wireless.getNetworkWirelessSsids(network_id)
        enabled_ssids = [s for s in ssids if s.get('enabled')]
        print(f"   ✅ Found {len(ssids)} SSIDs, {len(enabled_ssids)} enabled")
        results["successful"].append("get_network_wireless_ssids")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_ssids", str(e)))
    
    # 4. Get Network Devices
    try:
        print("\n4. Testing get_network_devices...")
        devices = meraki.dashboard.networks.getNetworkDevices(network_id)
        aps = [d for d in devices if d.get('model', '').startswith('MR')]
        print(f"   ✅ Found {len(devices)} devices, {len(aps)} APs")
        results["successful"].append("get_network_devices")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_devices", str(e)))
    
    # 5. Get Network Clients
    try:
        print("\n5. Testing get_network_clients...")
        clients = meraki.dashboard.networks.getNetworkClients(
            network_id, timespan=86400, perPage=1000, total_pages='all'
        )
        wireless_clients = [c for c in clients if c.get('ssid')]
        print(f"   ✅ Found {len(clients)} clients, {len(wireless_clients)} wireless")
        results["successful"].append("get_network_clients")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_clients", str(e)))
    
    # 6. Get Network Wireless Bluetooth Settings
    try:
        print("\n6. Testing get_network_wireless_bluetooth_settings...")
        bluetooth = meraki.dashboard.wireless.getNetworkWirelessBluetoothSettings(network_id)
        print(f"   ✅ Bluetooth scanning: {bluetooth.get('scanningEnabled', False)}")
        results["successful"].append("get_network_wireless_bluetooth_settings")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_bluetooth_settings", str(e)))
    
    # 7. Get Network Wireless RF Profiles
    try:
        print("\n7. Testing get_network_wireless_rf_profiles...")
        rf_profiles = meraki.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
        print(f"   ✅ Found {len(rf_profiles)} RF profiles")
        results["successful"].append("get_network_wireless_rf_profiles")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_rf_profiles", str(e)))
    
    # 8. Get Network Wireless Air Marshal
    try:
        print("\n8. Testing get_network_wireless_air_marshal...")
        air_marshal = meraki.dashboard.wireless.getNetworkWirelessAirMarshal(
            network_id, timespan=3600
        )
        print(f"   ✅ Found {len(air_marshal)} Air Marshal entries")
        results["successful"].append("get_network_wireless_air_marshal")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_air_marshal", str(e)))
    
    # 9. Get Network Events with productType
    try:
        print("\n9. Testing get_network_events with productType...")
        events = meraki.dashboard.networks.getNetworkEvents(
            network_id, productType='wireless', perPage=100
        )
        print(f"   ✅ Found {len(events) if events else 0} wireless events")
        results["successful"].append("get_network_events")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_events", str(e)))
    
    # 10. Get Network Wireless Connection Stats
    try:
        print("\n10. Testing get_network_wireless_connection_stats...")
        conn_stats = meraki.dashboard.wireless.getNetworkWirelessConnectionStats(
            network_id, timespan=3600
        )
        print(f"   ✅ Connection success rate: {conn_stats.get('assoc', 0)}%")
        results["successful"].append("get_network_wireless_connection_stats")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_connection_stats", str(e)))
    
    # 11. Get Network Wireless Latency Stats
    try:
        print("\n11. Testing get_network_wireless_latency_stats...")
        latency_stats = meraki.dashboard.wireless.getNetworkWirelessLatencyStats(
            network_id, timespan=3600
        )
        print(f"   ✅ Got latency stats")
        results["successful"].append("get_network_wireless_latency_stats")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_latency_stats", str(e)))
    
    # 12. Get Organization Devices Statuses (for better device status)
    try:
        print("\n12. Testing get_organization_devices_statuses...")
        device_statuses = meraki.dashboard.organizations.getOrganizationDevicesStatuses(
            org_id, perPage=1000, total_pages='all'
        )
        online_devices = [d for d in device_statuses if d.get('status') == 'online']
        print(f"   ✅ {len(online_devices)}/{len(device_statuses)} devices online")
        results["successful"].append("get_organization_devices_statuses")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_organization_devices_statuses", str(e)))
    
    # 13. Get Network Wireless SSID specific settings (for SSID 0)
    ssid_number = 0
    
    try:
        print(f"\n13. Testing SSID {ssid_number} Hotspot 2.0...")
        hotspot = meraki.dashboard.wireless.getNetworkWirelessSsidHotspot20(
            network_id, str(ssid_number)
        )
        print(f"   ✅ Hotspot 2.0 enabled: {hotspot.get('enabled', False)}")
        results["successful"].append("get_network_wireless_ssid_hotspot20")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_ssid_hotspot20", str(e)))
    
    try:
        print(f"\n14. Testing SSID {ssid_number} Splash Page...")
        splash = meraki.dashboard.wireless.getNetworkWirelessSsidSplashSettings(
            network_id, str(ssid_number)
        )
        print(f"   ✅ Splash page: {splash.get('splashPage', 'None')}")
        results["successful"].append("get_network_wireless_ssid_splash_settings")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_ssid_splash_settings", str(e)))
    
    # 15. Get Network Wireless Failed Connections
    try:
        print("\n15. Testing get_network_wireless_failed_connections...")
        failed_conns = meraki.dashboard.wireless.getNetworkWirelessFailedConnections(
            network_id, timespan=3600
        )
        print(f"   ✅ Found {len(failed_conns)} failed connections")
        results["successful"].append("get_network_wireless_failed_connections")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_failed_connections", str(e)))
    
    # 16. Get Network Wireless Mesh Statuses
    try:
        print("\n16. Testing get_network_wireless_mesh_statuses...")
        mesh_statuses = meraki.dashboard.wireless.getNetworkWirelessMeshStatuses(
            network_id, perPage=500, total_pages='all'  # Note: max 500 for mesh statuses
        )
        print(f"   ✅ Got mesh statuses")
        results["successful"].append("get_network_wireless_mesh_statuses")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_network_wireless_mesh_statuses", str(e)))
    
    # 17. Get Organization Wireless SSID Statuses by Device
    try:
        print("\n17. Testing get_organization_wireless_ssids_statuses_by_device...")
        ssid_statuses = meraki.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
            org_id, perPage=500, total_pages='all'  # Note: max 500 for SSID statuses
        )
        print(f"   ✅ Got SSID statuses for organization")
        results["successful"].append("get_organization_wireless_ssids_statuses_by_device")
    except Exception as e:
        print(f"   ❌ Failed: {str(e)[:100]}")
        results["failed"].append(("get_organization_wireless_ssids_statuses_by_device", str(e)))
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 WIFI AUDIT SUMMARY")
    print("=" * 70)
    print(f"\n✅ Successful Tools: {len(results['successful'])}")
    for tool in results['successful']:
        print(f"   • {tool}")
    
    print(f"\n❌ Failed Tools: {len(results['failed'])}")
    for tool, error in results['failed']:
        print(f"   • {tool}: {error[:80]}")
    
    print("\n" + "=" * 70)
    print(f"Success Rate: {len(results['successful'])}/{len(results['successful']) + len(results['failed'])} "
          f"({100 * len(results['successful']) / (len(results['successful']) + len(results['failed'])):.1f}%)")
    
    return results

if __name__ == "__main__":
    try:
        results = test_wifi_audit()
        print("\n✅ WiFi audit test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()