#!/usr/bin/env python3
"""
Comprehensive WiFi audit test - matches the exact transcript request.
Tests as many WiFi tools as possible to identify what works and what doesn't.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import traceback
from server.main import app, meraki

def test_comprehensive_wifi_audit():
    """
    Perform the most comprehensive WiFi audit possible.
    Tests ALL available wireless tools with proper parameters.
    """
    print("🚀 VERY EXTENSIVE WIFI AUDIT - SKYCOMM RESERVE ST")
    print("=" * 80)
    print("Testing ALL available WiFi tools with correct parameters...")
    
    # Configuration
    org_id = "686470"
    network_id = "L_726205439913500692"
    ssid_number = "0"  # Test SSID 0 (Apple)
    ap_serial = "Q2PD-JL52-H3B2"  # Office AP
    mx_serial = "Q2KY-NGXA-AJZU"  # Reserve St MX68
    
    results = {
        "successful": [],
        "failed": [],
        "total": 0
    }
    
    # Define all WiFi tools to test with proper parameters
    wifi_tools_to_test = [
        # Organization-level tools
        ("Get Organizations", lambda: meraki.dashboard.organizations.getOrganizations()),
        
        ("Get Organization Networks", lambda: meraki.dashboard.organizations.getOrganizationNetworks(
            org_id, perPage=1000, total_pages='all')),
        
        ("Get Organization Devices", lambda: meraki.dashboard.organizations.getOrganizationDevices(
            org_id, perPage=1000, total_pages='all')),
        
        ("Get Organization Device Statuses", lambda: meraki.dashboard.organizations.getOrganizationDevicesStatuses(
            org_id, perPage=1000, total_pages='all')),
        
        ("Get Organization Wireless Air Marshal Rules", lambda: meraki.dashboard.wireless.getOrganizationWirelessAirMarshalRules(
            org_id)),
        
        ("Get Organization Wireless SSID Statuses by Device", lambda: meraki.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
            org_id, perPage=500, total_pages='all')),  # Max 500 for SSID statuses
        
        # Network-level wireless tools
        ("Get Network Devices", lambda: meraki.dashboard.networks.getNetworkDevices(network_id)),
        
        ("Get Network Clients", lambda: meraki.dashboard.networks.getNetworkClients(
            network_id, timespan=86400, perPage=1000, total_pages='all')),
        
        ("Get Network Events (Wireless)", lambda: meraki.dashboard.networks.getNetworkEvents(
            network_id, productType='wireless', perPage=1000)),
        
        ("Get Network Wireless SSIDs", lambda: meraki.dashboard.wireless.getNetworkWirelessSsids(network_id)),
        
        ("Get Network Wireless RF Profiles", lambda: meraki.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)),
        
        ("Get Network Wireless Settings", lambda: meraki.dashboard.wireless.getNetworkWirelessSettings(network_id)),
        
        ("Get Network Wireless Bluetooth Settings", lambda: meraki.dashboard.wireless.getNetworkWirelessBluetoothSettings(network_id)),
        
        ("Get Network Wireless Air Marshal", lambda: meraki.dashboard.wireless.getNetworkWirelessAirMarshal(
            network_id, timespan=3600)),
        
        ("Get Network Wireless Connection Stats", lambda: meraki.dashboard.wireless.getNetworkWirelessConnectionStats(
            network_id, timespan=3600)),
        
        ("Get Network Wireless Latency Stats", lambda: meraki.dashboard.wireless.getNetworkWirelessLatencyStats(
            network_id, timespan=3600)),
        
        ("Get Network Wireless Failed Connections", lambda: meraki.dashboard.wireless.getNetworkWirelessFailedConnections(
            network_id, timespan=3600)),
        
        ("Get Network Wireless Client Count History", lambda: meraki.dashboard.wireless.getNetworkWirelessClientCountHistory(
            network_id, timespan=86400)),
        
        # Note: getNetworkWirelessBandwidthUsageHistory doesn't exist in SDK - removed
        
        ("Get Network Wireless Latency History", lambda: meraki.dashboard.wireless.getNetworkWirelessLatencyHistory(
            network_id, timespan=86400)),
        
        ("Get Network Wireless Mesh Statuses", lambda: meraki.dashboard.wireless.getNetworkWirelessMeshStatuses(
            network_id, perPage=500, total_pages='all')),  # Max 500 for mesh statuses
        
        ("Get Network Wireless Signal Quality History", lambda: meraki.dashboard.wireless.getNetworkWirelessSignalQualityHistory(
            network_id, deviceSerial=ap_serial, timespan=3600)),
        
        ("Get Network Wireless Usage History", lambda: meraki.dashboard.wireless.getNetworkWirelessUsageHistory(
            network_id, deviceSerial=ap_serial, timespan=3600)),
        
        ("Get Network Wireless Data Rate History", lambda: meraki.dashboard.wireless.getNetworkWirelessDataRateHistory(
            network_id, timespan=3600)),
        
        ("Get Network Wireless Channel Utilization History", lambda: meraki.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(
            network_id, deviceSerial=ap_serial, band='5', timespan=3600)),
        
        # SSID-specific tools (testing SSID 0)
        ("Get SSID Hotspot 2.0 Settings", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidHotspot20(
            network_id, ssid_number)),
        
        ("Get SSID Splash Settings", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidSplashSettings(
            network_id, ssid_number)),
        
        ("Get SSID Schedules", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidSchedules(
            network_id, ssid_number)),
        
        ("Get SSID VPN Settings", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidVpn(
            network_id, ssid_number)),
        
        ("Get SSID Bonjour Forwarding", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidBonjourForwarding(
            network_id, ssid_number)),
        
        ("Get SSID EAP Override", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidEapOverride(
            network_id, ssid_number)),
        
        ("Get SSID Device Type Group Policies", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(
            network_id, ssid_number)),
        
        ("Get SSID Identity PSKs", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidIdentityPsks(
            network_id, ssid_number)),
        
        ("Get SSID Traffic Shaping Rules", lambda: meraki.dashboard.wireless.getNetworkWirelessSsidTrafficShapingRules(
            network_id, ssid_number)),
        
        # Network wireless features
        ("Get Network Wireless Alternate Management Interface", lambda: meraki.dashboard.wireless.getNetworkWirelessAlternateManagementInterface(
            network_id)),
        
        ("Get Network Wireless Billing", lambda: meraki.dashboard.wireless.getNetworkWirelessBilling(network_id)),
        
        ("Get Network Wireless Electronic Shelf Label", lambda: meraki.dashboard.wireless.getNetworkWirelessElectronicShelfLabel(
            network_id)),
        
        ("Get Network Wireless Ethernet Ports Profiles", lambda: meraki.dashboard.wireless.getNetworkWirelessEthernetPortsProfiles(
            network_id)),
        
        # Device-specific tools (using Office AP)
        ("Get Device", lambda: meraki.dashboard.devices.getDevice(ap_serial)),
        
        ("Get Device Clients", lambda: meraki.dashboard.devices.getDeviceClients(
            ap_serial, timespan=86400)),
        
        ("Get Device Loss and Latency History", lambda: meraki.dashboard.devices.getDeviceLossAndLatencyHistory(
            mx_serial, ip='8.8.8.8', timespan=3600, resolution=60)),
        
        ("Get Device Management Interface", lambda: meraki.dashboard.devices.getDeviceManagementInterface(ap_serial)),
        
        ("Get Device LLDP CDP", lambda: meraki.dashboard.devices.getDeviceLldpCdp(ap_serial)),
        
        ("Get Device Wireless Bluetooth Settings", lambda: meraki.dashboard.wireless.getDeviceWirelessBluetoothSettings(
            ap_serial)),
        
        ("Get Device Wireless Radio Settings", lambda: meraki.dashboard.wireless.getDeviceWirelessRadioSettings(
            ap_serial)),
        
        ("Get Device Wireless Status", lambda: meraki.dashboard.wireless.getDeviceWirelessStatus(ap_serial)),
        
        ("Get Device Wireless Electronic Shelf Label", lambda: meraki.dashboard.wireless.getDeviceWirelessElectronicShelfLabel(
            ap_serial)),
        
        # Analytics and monitoring
        ("Get Organization Wireless Devices Ethernet Statuses", lambda: meraki.dashboard.wireless.getOrganizationWirelessDevicesEthernetStatuses(
            org_id, perPage=1000, total_pages='all')),
        
        ("Get Organization Wireless Devices Packet Loss by Client", lambda: meraki.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByClient(
            org_id, bands=['2.4', '5'], perPage=1000, total_pages='all')),
        
        ("Get Organization Wireless Devices Packet Loss by Device", lambda: meraki.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByDevice(
            org_id, bands=['2.4', '5'], perPage=1000, total_pages='all')),
        
        ("Get Organization Wireless Devices Packet Loss by Network", lambda: meraki.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByNetwork(
            org_id, bands=['2.4', '5'], perPage=1000, total_pages='all')),
        
        # Client-specific analytics (using actual client ID from the network)
        ("Get Network Wireless Client Connectivity Events", lambda: meraki.dashboard.wireless.getNetworkWirelessClientConnectivityEvents(
            network_id, clientId='k018068', perPage=1000, total_pages='all')),
        
        ("Get Network Wireless Client Connection Stats", lambda: meraki.dashboard.wireless.getNetworkWirelessClientConnectionStats(
            network_id, clientId='k018068', timespan=86400)),
        
        ("Get Network Wireless Client Latency History", lambda: meraki.dashboard.wireless.getNetworkWirelessClientLatencyHistory(
            network_id, clientId='k018068', timespan=86400)),
        
        ("Get Network Wireless Client Latency Stats", lambda: meraki.dashboard.wireless.getNetworkWirelessClientLatencyStats(
            network_id, clientId='k018068', timespan=86400)),
    ]
    
    # Run all tests
    print(f"\nTesting {len(wifi_tools_to_test)} WiFi tools...")
    print("-" * 80)
    
    for i, (tool_name, tool_func) in enumerate(wifi_tools_to_test, 1):
        results["total"] += 1
        try:
            print(f"\n{i:3}. Testing: {tool_name}...")
            result = tool_func()
            
            # Determine success based on result
            if result is not None:
                if isinstance(result, list):
                    print(f"     ✅ Success: Got {len(result)} items")
                elif isinstance(result, dict):
                    if 'errors' in result:
                        print(f"     ⚠️  API returned error: {result['errors']}")
                        results["failed"].append((tool_name, str(result['errors'])))
                    else:
                        print(f"     ✅ Success: Got data")
                else:
                    print(f"     ✅ Success: {type(result).__name__}")
                results["successful"].append(tool_name)
            else:
                print(f"     ⚠️  No data returned")
                results["successful"].append(tool_name)  # Still counts as successful API call
                
        except Exception as e:
            error_msg = str(e)[:150]
            print(f"     ❌ Failed: {error_msg}")
            results["failed"].append((tool_name, error_msg))
    
    # Print comprehensive summary
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE WIFI AUDIT RESULTS")
    print("=" * 80)
    
    success_rate = 100 * len(results['successful']) / results['total'] if results['total'] > 0 else 0
    
    print(f"\n✅ SUCCESSFUL TOOLS: {len(results['successful'])}/{results['total']} ({success_rate:.1f}%)")
    print("-" * 40)
    for tool in results['successful'][:20]:  # Show first 20
        print(f"  • {tool}")
    if len(results['successful']) > 20:
        print(f"  ... and {len(results['successful']) - 20} more")
    
    print(f"\n❌ FAILED TOOLS: {len(results['failed'])}")
    print("-" * 40)
    for tool, error in results['failed']:
        print(f"  • {tool}")
        print(f"    → {error[:100]}")
    
    # Categorize results
    print("\n📈 ANALYSIS BY CATEGORY:")
    print("-" * 40)
    
    categories = {
        "Organization": [t for t in results['successful'] if 'Organization' in t],
        "Network": [t for t in results['successful'] if 'Network' in t and 'SSID' not in t],
        "SSID": [t for t in results['successful'] if 'SSID' in t],
        "Device": [t for t in results['successful'] if 'Device' in t],
        "Analytics": [t for t in results['successful'] if any(x in t for x in ['History', 'Stats', 'Analytics'])],
        "Client": [t for t in results['successful'] if 'Client' in t],
    }
    
    for category, tools in categories.items():
        print(f"{category}: {len(tools)} tools working")
    
    print("\n" + "=" * 80)
    print(f"FINAL SCORE: {success_rate:.1f}% SUCCESS RATE")
    print("=" * 80)
    
    # Report tools that didn't work
    if results['failed']:
        print("\n⚠️  TOOLS THAT NEED ATTENTION:")
        print("-" * 40)
        for tool, error in results['failed']:
            if '404' in error:
                print(f"  • {tool} - Feature not available/configured")
            elif 'validation' in error.lower():
                print(f"  • {tool} - Parameter issue")
            elif 'attribute' in error.lower():
                print(f"  • {tool} - API method issue")
            else:
                print(f"  • {tool} - Other error")
    
    return results

if __name__ == "__main__":
    try:
        print("Testing comprehensive WiFi audit as MCP client would...")
        print("This simulates: 'do a very extensive wifi audit of skycomm reserve st'")
        print()
        results = test_comprehensive_wifi_audit()
        print(f"\n✅ Comprehensive WiFi audit test completed!")
        print(f"Success rate: {100 * len(results['successful']) / results['total']:.1f}%")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()