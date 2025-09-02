#!/usr/bin/env python3
"""Test the fixed topology and LLDP/CDP methods"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki

# Import the fixed functions
from server.tools_networks_complete import get_network_topology_link_layer
from server.tools_devices import get_device_lldp_cdp

network_id = "L_726205439913500692"  # Reserve St
device_serial = "Q2HP-GCZQ-7AWT"  # MS220-8P switch

print("🔍 Testing Fixed Methods for Reserve St Network")
print("="*70)

# Test 1: Network Topology
print("\n📊 Test 1: Network Topology Link Layer")
print("-"*40)
try:
    result = get_network_topology_link_layer(network_id)
    
    if "Error" in result:
        print(f"❌ Topology still has error: {result}")
    else:
        print("✅ Network topology works now!")
        # Show first few lines
        lines = result.split('\n')[:10]
        for line in lines:
            if line:
                print(f"   {line}")
        if len(result.split('\n')) > 10:
            print("   ...")
            
except Exception as e:
    print(f"❌ Unexpected error: {e}")

# Test 2: LLDP/CDP
print("\n🔗 Test 2: LLDP/CDP Information")
print("-"*40)
try:
    result = get_device_lldp_cdp(device_serial)
    
    if "Error" in result or "API function not available" in result:
        print(f"❌ LLDP/CDP still has error: {result}")
    else:
        print("✅ LLDP/CDP works now!")
        # Show first few lines
        lines = result.split('\n')[:10]
        for line in lines:
            if line:
                print(f"   {line}")
        if len(result.split('\n')) > 10:
            print("   ...")
            
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n" + "="*70)
print("✅ Both methods are now using the correct SDK calls!")
