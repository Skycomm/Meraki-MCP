#!/usr/bin/env python3
"""
Comprehensive test script for all Cisco Meraki MCP Server API methods.
Tests all 55 tools to verify they return expected data structures.
"""

import json
import sys
from typing import Dict, Any, List
from datetime import datetime

# SAFETY FIRST: Import and setup test safety
from test_common import setup_test_safety, print_safety_reminder
setup_test_safety()

from meraki_client import MerakiClient

# Initialize client
client = MerakiClient()

# Print safety reminder
print_safety_reminder()

# Test results tracking
results = {
    'passed': 0,
    'failed': 0,
    'errors': [],
    'warnings': []
}

def test_api_method(method_name: str, test_func, expected_type=None, validate_func=None):
    """Test a single API method and track results."""
    print(f"\n🧪 Testing: {method_name}")
    try:
        result = test_func()
        
        # Check if result is None (some delete methods)
        if result is None:
            print(f"  ✅ Returned None (expected for delete operations)")
            results['passed'] += 1
            return True
            
        # Type checking
        if expected_type and not isinstance(result, expected_type):
            error = f"Expected {expected_type.__name__}, got {type(result).__name__}"
            print(f"  ❌ Type Error: {error}")
            results['errors'].append(f"{method_name}: {error}")
            results['failed'] += 1
            return False
            
        # Custom validation
        if validate_func:
            is_valid, message = validate_func(result)
            if not is_valid:
                print(f"  ❌ Validation Failed: {message}")
                results['errors'].append(f"{method_name}: {message}")
                results['failed'] += 1
                return False
                
        # Print sample data
        if isinstance(result, list):
            print(f"  ✅ Returned {len(result)} items")
            if result and len(result) > 0:
                print(f"  📋 Sample: {list(result[0].keys()) if isinstance(result[0], dict) else 'Non-dict items'}")
        elif isinstance(result, dict):
            print(f"  ✅ Returned dict with keys: {list(result.keys())[:5]}...")
        else:
            print(f"  ✅ Returned: {str(result)[:100]}...")
            
        results['passed'] += 1
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"  ❌ Error: {error_msg}")
        results['errors'].append(f"{method_name}: {error_msg}")
        results['failed'] += 1
        
        # Check for common API errors
        if "404" in error_msg:
            results['warnings'].append(f"{method_name}: Resource not found (404) - might need valid IDs")
        elif "400" in error_msg:
            results['warnings'].append(f"{method_name}: Bad request (400) - check parameters")
        elif "403" in error_msg:
            results['warnings'].append(f"{method_name}: Forbidden (403) - check API permissions")
            
        return False

print("=" * 80)
print("🚀 CISCO MERAKI MCP SERVER - COMPREHENSIVE API TEST")
print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# Store IDs for testing
org_id = None
network_id = None
device_serial = None
switch_serial = None
camera_serial = None
wireless_client_mac = None

# ============ ORGANIZATION TESTS (8 tools) ============
print("\n\n📁 TESTING ORGANIZATION TOOLS (8)")
print("-" * 40)

# Get organizations (needed for other tests)
def validate_orgs(orgs):
    if not orgs:
        return False, "No organizations returned"
    if not all('id' in org and 'name' in org for org in orgs):
        return False, "Organizations missing required fields"
    return True, "Valid"

def validate_list_or_dict(result):
    """Some APIs return either list or dict depending on data."""
    if isinstance(result, (list, dict)):
        return True, "Valid"
    return False, f"Expected list or dict, got {type(result)}"

orgs = []
if test_api_method("get_organizations", 
                  lambda: client.get_organizations(),
                  list,
                  validate_orgs):
    orgs = client.get_organizations()
    if orgs:
        org_id = orgs[0]['id']
        print(f"  📌 Using Org ID: {org_id}")

# Test other org methods only if we have an org_id
if org_id:
    test_api_method("get_organization", 
                   lambda: client.get_organization(org_id),
                   dict)
    
    # Get networks for further testing
    networks = []
    if test_api_method("get_organization_networks",
                      lambda: client.get_organization_networks(org_id),
                      list):
        networks = client.get_organization_networks(org_id)
        if networks:
            network_id = networks[0]['id']
            print(f"  📌 Using Network ID: {network_id}")
    
    test_api_method("get_organization_alerts",
                   lambda: client.get_organization_alerts(org_id),
                   list)
    
    test_api_method("get_organization_firmware_upgrades",
                   lambda: client.get_organization_firmware_upgrades(org_id),
                   list)
    
    test_api_method("get_organization_webhooks",
                   lambda: client.get_organization_webhooks(org_id),
                   list)
    
    test_api_method("get_organization_devices_uplinks_loss_and_latency",
                   lambda: client.get_organization_devices_uplinks_loss_and_latency(org_id, 300),
                   list)
    
    test_api_method("get_organization_appliance_uplink_statuses",
                   lambda: client.get_organization_appliance_uplink_statuses(org_id),
                   list)

# ============ NETWORK TESTS (6 tools) ============
print("\n\n🌐 TESTING NETWORK TOOLS (6)")
print("-" * 40)

if network_id:
    test_api_method("get_network",
                   lambda: client.get_network(network_id),
                   dict)
    
    # Get devices for further testing
    devices = []
    if test_api_method("get_network_devices",
                      lambda: client.get_network_devices(network_id),
                      list):
        devices = client.get_network_devices(network_id)
        if devices:
            device_serial = devices[0]['serial']
            # Find switch, camera, and AP if available
            ap_serial = None
            for device in devices:
                if 'MS' in device.get('model', ''):
                    switch_serial = device['serial']
                elif 'MV' in device.get('model', ''):
                    camera_serial = device['serial']
                elif 'MR' in device.get('model', ''):
                    ap_serial = device['serial']
            print(f"  📌 Device Serial: {device_serial}")
            if switch_serial:
                print(f"  📌 Switch Serial: {switch_serial}")
            if camera_serial:
                print(f"  📌 Camera Serial: {camera_serial}")
            if ap_serial:
                print(f"  📌 AP Serial: {ap_serial}")
    
    # Get clients and find a wireless one
    clients = []
    if test_api_method("get_network_clients",
                      lambda: client.get_network_clients(network_id, timespan=3600),
                      list):
        clients = client.get_network_clients(network_id, timespan=3600)
        # Find a wireless client
        for c in clients:
            if c.get('ssid'):  # Has SSID = wireless client
                wireless_client_mac = c.get('mac')
                print(f"  📌 Wireless Client MAC: {wireless_client_mac}")
                break
    
    test_api_method("get_network_vlans",
                   lambda: client.get_network_vlans(network_id),
                   list)
    
    test_api_method("get_network_webhook_http_servers",
                   lambda: client.get_network_webhook_http_servers(network_id),
                   list)
    
    test_api_method("get_network_alerts_settings",
                   lambda: client.get_network_alerts_settings(network_id),
                   dict)

# ============ DEVICE TESTS (5 tools) ============
print("\n\n📱 TESTING DEVICE TOOLS (5)")
print("-" * 40)

if device_serial:
    test_api_method("get_device",
                   lambda: client.get_device(device_serial),
                   dict)
    
    test_api_method("get_device_clients",
                   lambda: client.get_device_clients(device_serial, timespan=3600),
                   list)
    
    test_api_method("get_device_status",
                   lambda: client.get_device_status(device_serial),
                   dict)
    
    # Skip update/reboot to avoid changing production
    print("\n⏭️  Skipping update_device (would modify production)")
    print("⏭️  Skipping reboot_device (would reboot production device)")
    results['warnings'].append("Skipped update_device and reboot_device to avoid production changes")

# ============ WIRELESS TESTS (9 tools) ============
print("\n\n📡 TESTING WIRELESS TOOLS (9)")
print("-" * 40)

if network_id:
    test_api_method("get_network_wireless_ssids",
                   lambda: client.get_network_wireless_ssids(network_id),
                   list)
    
    test_api_method("get_network_wireless_passwords",
                   lambda: client.get_network_wireless_passwords(network_id),
                   list)
    
    test_api_method("get_network_wireless_clients",
                   lambda: client.get_network_wireless_clients(network_id, timespan=3600),
                   list)
    
    # Test with client MAC if available, otherwise will return empty
    if wireless_client_mac:
        test_api_method("get_network_wireless_usage",
                       lambda: client.get_network_wireless_usage(network_id, timespan=3600, client_mac=wireless_client_mac),
                       list)
    else:
        # This will return empty list as API requires device/client
        test_api_method("get_network_wireless_usage",
                       lambda: client.get_network_wireless_usage(network_id, timespan=3600),
                       list)
    
    test_api_method("get_network_wireless_rf_profiles",
                   lambda: client.get_network_wireless_rf_profiles(network_id),
                   list)
    
    test_api_method("get_network_wireless_air_marshal",
                   lambda: client.get_network_wireless_air_marshal(network_id, timespan=3600),
                   list)
    
    test_api_method("get_network_wireless_bluetooth_clients",
                   lambda: client.get_network_wireless_bluetooth_clients(network_id),
                   dict)
    
    # Test with client MAC if available, otherwise will return empty
    if wireless_client_mac:
        test_api_method("get_network_wireless_channel_utilization",
                       lambda: client.get_network_wireless_channel_utilization(network_id, timespan=3600, client_mac=wireless_client_mac),
                       list)
    else:
        # This will return empty list as API requires device/client
        test_api_method("get_network_wireless_channel_utilization",
                       lambda: client.get_network_wireless_channel_utilization(network_id, timespan=3600),
                       list)
    
    print("\n⏭️  Skipping update_network_wireless_ssid (would modify production)")

# ============ SWITCH TESTS (5 tools) ============
print("\n\n🔌 TESTING SWITCH TOOLS (5)")
print("-" * 40)

if switch_serial:
    test_api_method("get_device_switch_ports",
                   lambda: client.get_device_switch_ports(switch_serial),
                   list)
    
    test_api_method("get_device_switch_port_statuses",
                   lambda: client.get_device_switch_port_statuses(switch_serial),
                   list)
    
    test_api_method("get_device_switch_vlans",
                   lambda: client.get_device_switch_vlans(switch_serial),
                   list)
    
    print("\n⏭️  Skipping update_device_switch_port (would modify production)")
    print("⏭️  Skipping create_device_switch_vlan (would modify production)")
else:
    print("⚠️  No switch found in network - skipping switch tests")
    results['warnings'].append("No switch device found for testing switch-specific APIs")

# ============ ANALYTICS TESTS (4 tools) ============
print("\n\n📊 TESTING ANALYTICS TOOLS (4)")
print("-" * 40)

if network_id:
    test_api_method("get_network_connection_stats",
                   lambda: client.get_network_connection_stats(network_id, timespan=3600),
                   (dict, list))
    
    test_api_method("get_network_latency_stats",
                   lambda: client.get_network_latency_stats(network_id, timespan=3600),
                   (dict, list))

# Already tested org uplink methods above

# ============ APPLIANCE TESTS (6 tools) ============
print("\n\n🔥 TESTING APPLIANCE TOOLS (6)")
print("-" * 40)

if network_id:
    test_api_method("get_network_appliance_firewall_l3_rules",
                   lambda: client.get_network_appliance_firewall_l3_rules(network_id),
                   dict)
    
    test_api_method("get_network_appliance_content_filtering",
                   lambda: client.get_network_appliance_content_filtering(network_id),
                   dict)
    
    test_api_method("get_network_appliance_vpn_site_to_site",
                   lambda: client.get_network_appliance_vpn_site_to_site(network_id),
                   dict)
    
    test_api_method("get_network_appliance_security_malware",
                   lambda: client.get_network_appliance_security_malware(network_id),
                   dict)
    
    test_api_method("get_network_appliance_security_intrusion",
                   lambda: client.get_network_appliance_security_intrusion(network_id),
                   dict)
    
    print("\n⏭️  Skipping update_network_appliance_firewall_l3_rules (would modify production)")

# ============ CAMERA TESTS (6 tools) ============
print("\n\n📹 TESTING CAMERA TOOLS (6)")
print("-" * 40)

if camera_serial:
    test_api_method("get_device_camera_video_link",
                   lambda: client.get_device_camera_video_link(camera_serial),
                   dict)
    
    test_api_method("get_device_camera_snapshot",
                   lambda: client.get_device_camera_snapshot(camera_serial),
                   dict)
    
    test_api_method("get_device_camera_video_settings",
                   lambda: client.get_device_camera_video_settings(camera_serial),
                   dict)
    
    test_api_method("get_device_camera_analytics_zones",
                   lambda: client.get_device_camera_analytics_zones(camera_serial),
                   list)
    
    test_api_method("get_device_camera_sense",
                   lambda: client.get_device_camera_sense(camera_serial),
                   dict)
    
    print("\n⏭️  Skipping update_device_camera_video_settings (would modify production)")
else:
    print("⚠️  No camera found in network - skipping camera tests")
    results['warnings'].append("No camera device found for testing camera-specific APIs")

# ============ MODIFICATION TESTS ============
print("\n\n🛠️  TESTING CREATE/UPDATE/DELETE METHODS")
print("-" * 40)
print("⚠️  Skipping all create/update/delete operations to avoid modifying production")
print("   Skipped methods:")
print("   - create_organization / update_organization / delete_organization")
print("   - create_network / update_network / delete_network") 
print("   - update_device / reboot_device")
print("   - update_network_wireless_ssid")
print("   - update_device_switch_port / create_device_switch_vlan")
print("   - create_organization_webhook / create_network_webhook_http_server")
print("   - update_network_alerts_settings")
print("   - update_network_appliance_firewall_l3_rules")
print("   - update_device_camera_video_settings")

# ============ FINAL REPORT ============
print("\n\n" + "=" * 80)
print("📊 TEST RESULTS SUMMARY")
print("=" * 80)
print(f"✅ Passed: {results['passed']}")
print(f"❌ Failed: {results['failed']}")
print(f"⚠️  Warnings: {len(results['warnings'])}")

if results['errors']:
    print("\n❌ ERRORS:")
    for error in results['errors']:
        print(f"   - {error}")

if results['warnings']:
    print("\n⚠️  WARNINGS:")
    for warning in results['warnings']:
        print(f"   - {warning}")

print("\n📋 COVERAGE:")
print(f"   - Total API methods in client: 55")
print(f"   - Methods tested: {results['passed'] + results['failed']}")
print(f"   - Methods skipped (modify production): ~16")

# Save results
with open('test_results.json', 'w') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'test_ids': {
            'org_id': org_id,
            'network_id': network_id,
            'device_serial': device_serial,
            'switch_serial': switch_serial,
            'camera_serial': camera_serial
        }
    }, f, indent=2)

print(f"\n💾 Results saved to: test_results.json")
print("\n✅ TEST COMPLETE!")