#!/usr/bin/env python3
"""
Check SSID 1 specifically since the screenshot shows "SSID 1" with WPA2 PSK.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def check_ssid_1():
    """Check SSID 1 configuration specifically."""
    
    print("🧪 CHECKING SSID 1 SPECIFICALLY")
    print("=" * 50)
    
    meraki_client = MerakiClient()
    network_id = 'L_669347494617957322'
    
    print("From screenshot: SSID 1 shows:")
    print("- Status: Enabled ✓") 
    print("- Name: Mercy Bariatrics")
    print("- Security: WPA2 PSK ✓")
    print("- WPA key: ••••••••••••••••• (password protected)")
    print("- WPA encryption mode: WPA2 only ✓")
    print("- Visibility: Advertise this SSID publicly ✓")
    print()
    
    print("API Check for SSID 1:")
    print("-" * 30)
    
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsid(
            network_id, '1'  # SSID 1 specifically
        )
        
        print(f"Name: {result.get('name', 'Unknown')}")
        print(f"Number: {result.get('number', 'Unknown')}")
        print(f"Enabled: {result.get('enabled', False)}")
        print(f"Auth Mode: {result.get('authMode', 'Unknown')}")
        print(f"WPA Encryption: {result.get('wpaEncryptionMode', 'N/A')}")
        print(f"Visible: {result.get('visible', 'N/A')}")
        print(f"SSID Admin Accessible: {result.get('ssidAdminAccessible', 'N/A')}")
        
        # Check if this matches screenshot
        name = result.get('name', '')
        enabled = result.get('enabled', False)
        auth_mode = result.get('authMode', '')
        
        print(f"\n🔍 Comparison with Screenshot:")
        print(f"   Name match: {'✅' if 'mercy' in name.lower() or 'bariatrics' in name.lower() else '❌'} (Expected: Mercy Bariatrics)")
        print(f"   Enabled: {'✅' if enabled else '❌'}")
        print(f"   Security: {'✅ WPA2' if auth_mode == 'psk' else f'❌ {auth_mode.upper()}'}")
        
        if auth_mode == 'psk':
            print("🎉 FOUND IT! SSID 1 has WPA2 PSK security!")
        else:
            print(f"🤔 SSID 1 shows {auth_mode}, not WPA2 PSK")
            
        print(f"\n📊 All SSID 1 fields:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error checking SSID 1: {e}")

if __name__ == "__main__":
    check_ssid_1()