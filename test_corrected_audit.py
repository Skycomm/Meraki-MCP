#!/usr/bin/env python3
"""
Test the corrected audit behavior for MX*W integrated wireless.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

# Initialize the client
meraki_client = MerakiClient()

def test_audit_logic():
    """Test the corrected audit logic for MX*W networks."""
    
    print("🧪 TESTING CORRECTED AUDIT LOGIC")
    print("=" * 60)
    
    network_id = 'L_669347494617957322'  # Mercy Bariatrics MX65W
    
    try:
        # Get network details
        network = meraki_client.dashboard.networks.getNetwork(network_id)
        network_name = network.get('name', 'Unknown')
        product_types = network.get('productTypes', [])
        
        print(f"Network: {network_name}")
        print(f"Product Types: {product_types}")
        
        # Get devices to understand infrastructure
        devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
        
        mx_with_wifi = []
        mr_devices = []
        
        for device in devices:
            model = device.get('model', '')
            if model.startswith('MX') and ('W' in model or 'w' in model):
                mx_with_wifi.append(device)
                print(f"✅ MX with WiFi: {model}")
            elif model.startswith('MR'):
                mr_devices.append(device)
                print(f"📡 MR device: {model}")
        
        print(f"\nInfrastructure Analysis:")
        print(f"  MX with WiFi: {len(mx_with_wifi)}")
        print(f"  MR devices: {len(mr_devices)}")
        
        # Test audit logic
        print(f"\n🔍 Audit Logic Decision:")
        
        if 'wireless' not in product_types:
            print("❌ No wireless capability - would skip wireless checks")
        elif 'wireless' in product_types and mr_devices:
            print("✅ Has wireless + MR devices - would check wireless connection stats")
        elif 'wireless' in product_types and mx_with_wifi and not mr_devices:
            print("✅ MX-only wireless - would note integrated wireless, skip wireless connection stats")
            mx_model = mx_with_wifi[0].get('model', 'MX*W')
            print(f"   WiFi Source: {mx_model} integrated wireless")
            print(f"   Note: No separate access points to monitor")
        else:
            print("⚠️  Other scenario")
        
        # Test SSID check - this should still work
        print(f"\n📶 SSID Check:")
        try:
            ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
            enabled_count = len([s for s in ssids if s.get('enabled')])
            print(f"✅ SSID API works: {enabled_count} enabled SSIDs")
            
            for ssid in ssids:
                if ssid.get('enabled'):
                    name = ssid.get('name', 'Unnamed')
                    auth = ssid.get('authMode', 'unknown')
                    print(f"   SSID: {name} ({auth})")
                    
        except Exception as e:
            print(f"❌ SSID API error: {e}")
        
        # Test wireless connection stats (should work but may return empty)
        print(f"\n📊 Wireless Connection Stats:")
        try:
            conn_stats = meraki_client.dashboard.wireless.getNetworkWirelessConnectionStats(
                network_id, timespan=3600
            )
            if conn_stats:
                success = conn_stats.get('success', 0)
                total = sum([conn_stats.get(k, 0) for k in ['success', 'auth', 'assoc', 'dhcp', 'dns']])
                print(f"✅ Connection stats available: {success}/{total} success rate")
            else:
                print(f"ℹ️ No connection stats available (expected for MX integrated)")
        except Exception as e:
            print(f"⚠️ Connection stats error: {e}")
            print(f"   This is expected for MX-only networks")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_audit_logic()