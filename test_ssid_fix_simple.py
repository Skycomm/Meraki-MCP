#!/usr/bin/env python3
"""
Simple test to validate SSID security detection using the client directly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

def test_ssid_security():
    """Test SSID security detection directly via API."""
    
    print("🧪 TESTING SSID SECURITY DETECTION")
    print("=" * 50)
    
    # Initialize client
    meraki_client = MerakiClient()
    
    # Mercy Bariatrics network
    network_id = 'L_669347494617957322'  
    ssid_number = '0'  # First SSID
    
    try:
        # Get SSID details directly
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsid(
            network_id, ssid_number
        )
        
        print(f"Network ID: {network_id}")
        print(f"SSID Number: {ssid_number}")
        print("\n📋 Raw SSID Data:")
        print(f"Name: {result.get('name', 'Unknown')}")
        print(f"Enabled: {result.get('enabled', False)}")
        print(f"Auth Mode: {result.get('authMode', 'Unknown')}")
        print(f"WPA Encryption: {result.get('wpaEncryptionMode', 'N/A')}")
        print(f"Visible: {result.get('visible', 'N/A')}")
        
        # Security analysis
        auth_mode = result.get('authMode', 'Unknown')
        print(f"\n🔐 Security Analysis:")
        
        if auth_mode == 'psk':
            print("✅ SECURE: WPA/WPA2 Personal (PSK) detected")
            wpa_mode = result.get('wpaEncryptionMode', 'Unknown')
            print(f"   Encryption: {wpa_mode}")
        elif auth_mode == 'open':
            print("❌ INSECURE: Open network (no password)")
        else:
            print(f"⚠️  OTHER: {auth_mode}")
            
        print(f"\n📊 Full result keys: {list(result.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_ssid_security()