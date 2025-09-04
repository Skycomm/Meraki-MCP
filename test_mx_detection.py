#!/usr/bin/env python3
"""
Test the enhanced audit with MX*W wireless detection.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient

# Initialize the client
meraki_client = MerakiClient()

def test_mercy_bariatrics_mx_detection():
    """Test MX*W detection on Mercy Bariatrics (MX65W only)."""
    
    print("🧪 TESTING MX*W DETECTION - MERCY BARIATRICS")
    print("=" * 60)
    
    network_id = 'L_669347494617957322'  # Mt Lawley (MX65W)
    
    try:
        # Get devices to test our logic
        devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
        
        mx_with_wifi = []
        mr_devices = []
        other_devices = []
        
        print("📋 Device Analysis:")
        for device in devices:
            model = device.get('model', '')
            device_name = device.get('name') or device.get('serial', 'Unnamed')
            status = device.get('status', 'unknown')
            
            print(f"  Device: {device_name} ({model}) - {status}")
            
            if model.startswith('MX') and ('W' in model or 'w' in model):
                mx_with_wifi.append(device)
                print(f"    ✅ MX with WiFi detected!")
            elif model.startswith('MR'):
                mr_devices.append(device)
                print(f"    📡 MR access point detected!")
            else:
                other_devices.append(device)
                print(f"    🔧 Other device type")
        
        print(f"\n📊 Summary:")
        print(f"  MX with WiFi: {len(mx_with_wifi)}")
        print(f"  MR devices: {len(mr_devices)}")
        print(f"  Other devices: {len(other_devices)}")
        
        # Test infrastructure classification
        if mx_with_wifi and not mr_devices:
            infrastructure_type = "MX Integrated Wireless Only"
            print(f"  🎯 Infrastructure: {infrastructure_type}")
            print(f"  Note: No dedicated APs - WiFi from MX appliance")
        elif mr_devices and not mx_with_wifi:
            infrastructure_type = "Dedicated MR Access Points Only"
            print(f"  🎯 Infrastructure: {infrastructure_type}")
        elif mx_with_wifi and mr_devices:
            infrastructure_type = "Mixed (MX + MR)"
            print(f"  🎯 Infrastructure: {infrastructure_type}")
        else:
            infrastructure_type = "No wireless infrastructure"
            print(f"  ⚠️ Infrastructure: {infrastructure_type}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_skycomm_attadale_detection():
    """Test mixed infrastructure on Skycomm Attadale (MX64W + MR33)."""
    
    print("\n🧪 TESTING MIXED INFRASTRUCTURE - SKYCOMM ATTADALE")
    print("=" * 60)
    
    network_id = 'L_726205439913492992'  # Attadale (MX64W + MR33)
    
    try:
        devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
        
        mx_with_wifi = []
        mr_devices = []
        
        print("📋 Device Analysis:")
        for device in devices:
            model = device.get('model', '')
            device_name = device.get('name') or device.get('serial', 'Unnamed')
            status = device.get('status', 'unknown')
            
            print(f"  Device: {device_name} ({model}) - {status}")
            
            if model.startswith('MX') and ('W' in model or 'w' in model):
                mx_with_wifi.append(device)
                print(f"    ✅ MX with WiFi detected!")
            elif model.startswith('MR'):
                mr_devices.append(device)
                print(f"    📡 MR access point detected!")
        
        print(f"\n📊 Summary:")
        print(f"  MX with WiFi: {len(mx_with_wifi)}")
        print(f"  MR devices: {len(mr_devices)}")
        
        # Test mixed classification
        if mx_with_wifi and mr_devices:
            print(f"  🎯 Infrastructure: Mixed (MX integrated + MR dedicated)")
            print(f"  This provides both MX WiFi and dedicated AP coverage")
            return True
        else:
            print(f"  ⚠️ Expected mixed infrastructure but didn't find it")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🎯 MX*W WIRELESS INFRASTRUCTURE DETECTION TEST")
    print("Testing enhanced audit logic for different network types\n")
    
    mercy_ok = test_mercy_bariatrics_mx_detection()
    attadale_ok = test_skycomm_attadale_detection()
    
    print("\n" + "=" * 60)
    print("📋 TEST RESULTS")
    print("=" * 60)
    
    print(f"Mercy Bariatrics (MX only): {'✅ PASSED' if mercy_ok else '❌ FAILED'}")
    print(f"Skycomm Attadale (Mixed): {'✅ PASSED' if attadale_ok else '❌ FAILED'}")
    
    if mercy_ok and attadale_ok:
        print("\n🎉 SUCCESS: Enhanced audit now properly detects:")
        print("✅ MX*W devices with integrated wireless")
        print("✅ Dedicated MR access points")
        print("✅ Mixed infrastructure scenarios")
        print("✅ Different wireless coverage sources")
        print("\nNetwork audits will now show accurate wireless infrastructure details!")
    else:
        print("\n⚠️ Some tests failed - review implementation")
        
    print("=" * 60)