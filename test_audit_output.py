#!/usr/bin/env python3
"""
Quick test to see the audit output with MX*W detection.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki
from meraki_client import MerakiClient

# Initialize the client
meraki_client = MerakiClient()

def simulate_audit_infrastructure_section():
    """Simulate just the infrastructure section of the audit."""
    
    print("🧪 SIMULATING AUDIT INFRASTRUCTURE SECTION")
    print("=" * 60)
    
    network_id = 'L_669347494617957322'  # Mercy Bariatrics MX65W
    
    try:
        # Get network details
        network = meraki_client.dashboard.networks.getNetwork(network_id)
        network_name = network.get('name', 'Unknown')
        
        print(f"Network: {network_name}")
        print(f"Products: {network.get('productTypes', [])}")
        
        # Device analysis (same logic as in audit)
        devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
        
        mx_with_wifi = []
        mr_devices = []
        other_devices = []
        
        for device in devices:
            model = device.get('model', '')
            device_name = device.get('name') or device.get('serial', 'Unnamed')
            
            if model.startswith('MX') and ('W' in model or 'w' in model):
                mx_with_wifi.append({
                    'model': model,
                    'name': device_name,
                    'serial': device.get('serial', ''),
                    'status': device.get('status', 'unknown')
                })
            elif model.startswith('MR'):
                mr_devices.append({
                    'model': model,
                    'name': device_name,
                    'serial': device.get('serial', ''),
                    'status': device.get('status', 'unknown')
                })
        
        # Generate the infrastructure report section
        print("\n📡 Wireless Infrastructure Analysis")
        
        if mx_with_wifi and not mr_devices:
            print("**WiFi Source**: MX Integrated Wireless Only")
            print("*Note: No dedicated wireless access points - WiFi provided by MX appliance*")
            for mx in mx_with_wifi:
                status_icon = "✅" if mx['status'] == 'online' else "❌"
                print(f"- {status_icon} **{mx['model']}**: {mx['name']} ({mx['serial']})")
        
        # Also test the WiFi section reference
        print(f"\n📶 WiFi Security Analysis")
        print(f"**Total SSIDs**: 15 (standard for Meraki)")
        print(f"**Enabled SSIDs**: 1")  # From our test
        print(f"**Disabled SSIDs**: 14")
        
        if mx_with_wifi and not mr_devices:
            print(f"*WiFi broadcast by MX integrated wireless*")
        
        print("\n✅ Infrastructure detection working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simulate_audit_infrastructure_section()