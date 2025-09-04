#!/usr/bin/env python3
"""
Test script to validate the fixed wireless SSID tool.
This should now properly detect WPA2 PSK security on Mercy Bariatrics SSID.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki
from server.tools_SDK_wireless import get_network_wireless_ssid

def test_mercy_bariatrics_ssid():
    """Test the fixed SSID tool with Mercy Bariatrics network."""
    
    print("🧪 TESTING FIXED WIRELESS SSID TOOL")
    print("=" * 50)
    
    # Mercy Bariatrics network and SSID
    network_id = 'L_669347494617957322'  # Mt Lawley network
    ssid_number = '0'  # First SSID (should be the active one)
    
    print(f"Testing Network: {network_id}")
    print(f"SSID Number: {ssid_number}")
    print("Expected: WPA2 PSK security (not open)")
    print()
    
    try:
        # Test the fixed tool function directly
        result = get_network_wireless_ssid(network_id, ssid_number)
        
        print("🔍 SSID Security Analysis:")
        print("-" * 40)
        print(result)
        print("-" * 40)
        
        # Check for security indicators
        if "WPA/WPA2 Personal (PSK)" in result:
            print("✅ SUCCESS: Correctly detected WPA2 PSK security!")
        elif "Open (No Password Protection)" in result:
            print("❌ FAIL: Still incorrectly reporting as open network")
        else:
            print("⚠️  UNCLEAR: Security detection needs review")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing SSID tool: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 WIRELESS SSID SECURITY DETECTION FIX TEST")
    print("Validating that WPA2 PSK is now properly detected\n")
    
    success = test_mercy_bariatrics_ssid()
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if success:
        print("✅ Test completed - check output above for security detection")
        print("🏥 For Mercy Bariatrics: Should show WPA2 PSK, not open network")
    else:
        print("❌ Test failed - tool still has issues")
        
    print("=" * 50)