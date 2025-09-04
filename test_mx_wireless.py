#!/usr/bin/env python3
"""
Test MX device wireless capabilities and SSID configuration.
The MX65W has built-in wireless that might use different API endpoints.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def test_mx_wireless():
    """Check MX device wireless configuration."""
    
    print("🧪 TESTING MX DEVICE WIRELESS CAPABILITIES")
    print("=" * 60)
    
    meraki_client = MerakiClient()
    network_id = 'L_669347494617957322'
    device_serial = 'Q2RN-VSLD-4JEG'  # MX65W device
    
    print(f"Network: {network_id}")
    print(f"Device: {device_serial} (MX65W)")
    print()
    
    # Check network product types
    print("1. 📋 Network Product Types:")
    try:
        network_info = meraki_client.dashboard.networks.getNetwork(network_id)
        product_types = network_info.get('productTypes', [])
        print(f"   Product Types: {product_types}")
        
        has_wireless = 'wireless' in product_types
        has_appliance = 'appliance' in product_types
        print(f"   Has Wireless: {has_wireless}")
        print(f"   Has Appliance: {has_appliance}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Check device details
    print("2. 🛡️ MX Device Details:")
    try:
        device_info = meraki_client.dashboard.devices.getDevice(device_serial)
        print(f"   Model: {device_info.get('model', 'Unknown')}")
        print(f"   Name: {device_info.get('name', 'Unnamed')}")
        print(f"   Network ID: {device_info.get('networkId', 'Unknown')}")
        
        # Check if wireless is mentioned in device tags/details
        tags = device_info.get('tags', [])
        if tags:
            print(f"   Tags: {tags}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Try appliance wireless endpoints
    print("3. 📶 Appliance Wireless Configuration:")
    try:
        # This might be where MX wireless config lives
        appliance_wireless = meraki_client.dashboard.appliance.getNetworkApplianceSettings(network_id)
        print(f"   Appliance Settings Keys: {list(appliance_wireless.keys())}")
        
        # Look for wireless-related keys
        wireless_keys = [k for k in appliance_wireless.keys() if 'wireless' in k.lower() or 'wifi' in k.lower() or 'ssid' in k.lower()]
        if wireless_keys:
            print(f"   Wireless-related keys: {wireless_keys}")
            for key in wireless_keys:
                print(f"     {key}: {appliance_wireless.get(key)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Try device-specific wireless settings
    print("4. 🔍 Device-Specific Wireless:")
    try:
        # Some MX devices have device-specific wireless settings
        device_wireless = meraki_client.dashboard.devices.getDeviceWirelessStatus(device_serial)
        print(f"   Wireless Status: {device_wireless}")
    except Exception as e:
        print(f"   ❌ Device wireless status error: {e}")
    
    # Check if there are MX-specific wireless endpoints
    print("\n5. 🔧 Alternative Wireless Endpoints:")
    
    # Try getting wireless settings through different paths
    endpoints_to_try = [
        ("Network Wireless Settings", lambda: meraki_client.dashboard.wireless.getNetworkWirelessSettings(network_id)),
        ("Network Wireless SSIDs", lambda: meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)),
    ]
    
    for name, endpoint_func in endpoints_to_try:
        try:
            result = endpoint_func()
            print(f"   ✅ {name}: Found {len(result) if isinstance(result, list) else 'data'}")
            if name == "Network Wireless SSIDs" and isinstance(result, list):
                for ssid in result:
                    if ssid.get('enabled'):
                        ssid_name = ssid.get('name', 'Unnamed')
                        auth_mode = ssid.get('authMode', 'Unknown')
                        ssid_num = ssid.get('number', 'Unknown')
                        print(f"     SSID {ssid_num}: {ssid_name} ({auth_mode})")
        except Exception as e:
            print(f"   ❌ {name}: {e}")

if __name__ == "__main__":
    test_mx_wireless()