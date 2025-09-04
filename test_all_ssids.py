#!/usr/bin/env python3
"""
Check all SSIDs on Mercy Bariatrics network to find which one has WPA2.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def check_all_ssids():
    """Check all SSID numbers to find WPA2 configuration."""
    
    print("🧪 CHECKING ALL SSIDS ON MERCY BARIATRICS NETWORK")
    print("=" * 60)
    
    meraki_client = MerakiClient()
    network_id = 'L_669347494617957322'
    
    print(f"Network ID: {network_id}")
    print("\n📡 Scanning all SSID numbers (0-14)...")
    
    wpa_ssids = []
    open_ssids = []
    
    for ssid_num in range(15):  # Check SSID 0-14
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsid(
                network_id, str(ssid_num)
            )
            
            name = result.get('name', f'SSID {ssid_num}')
            enabled = result.get('enabled', False)
            auth_mode = result.get('authMode', 'Unknown')
            
            print(f"  SSID {ssid_num}: {name}")
            print(f"    Enabled: {enabled}")
            print(f"    Security: {auth_mode}")
            
            if enabled:
                if auth_mode == 'psk':
                    wpa_ssids.append((ssid_num, name, result.get('wpaEncryptionMode', 'Unknown')))
                    print(f"    ✅ WPA/WPA2 detected!")
                elif auth_mode == 'open':
                    open_ssids.append((ssid_num, name))
                    print(f"    ❌ Open network")
                else:
                    print(f"    ⚪ Other: {auth_mode}")
            print()
            
        except Exception as e:
            print(f"  SSID {ssid_num}: Error - {str(e)}")
    
    print("=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    if wpa_ssids:
        print("✅ WPA/WPA2 Protected SSIDs:")
        for ssid_num, name, encryption in wpa_ssids:
            print(f"   SSID {ssid_num}: {name} ({encryption})")
    else:
        print("❌ No WPA/WPA2 protected SSIDs found")
    
    if open_ssids:
        print("\n⚠️ Open Network SSIDs:")
        for ssid_num, name in open_ssids:
            print(f"   SSID {ssid_num}: {name}")
    
    print(f"\n🤔 Conclusion:")
    if wpa_ssids:
        print(f"   The screenshot might show SSID {wpa_ssids[0][0]} with WPA2")
    else:
        print("   Configuration mismatch: UI shows WPA2, but API shows all as open/other")

if __name__ == "__main__":
    check_all_ssids()