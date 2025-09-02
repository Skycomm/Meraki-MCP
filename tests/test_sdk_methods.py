#!/usr/bin/env python3
"""Test what SDK methods are available for topology and LLDP/CDP"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki

# Check what methods are available for network topology
print("Checking network topology methods:")
print("-"*40)
network_methods = [m for m in dir(meraki.dashboard.networks) if 'topology' in m.lower()]
print(f"Network topology methods: {network_methods}")

# Check what methods are available for LLDP/CDP
print("\nChecking LLDP/CDP methods:")
print("-"*40)
device_methods = [m for m in dir(meraki.dashboard.devices) if 'lldp' in m.lower() or 'cdp' in m.lower()]
print(f"Device LLDP/CDP methods: {device_methods}")

# Try to find the correct methods
print("\nTrying actual SDK calls:")
print("-"*40)

network_id = "L_726205439913500692"  # Reserve St
device_serial = "Q2HP-GCZQ-7AWT"  # MS220-8P switch

# Try network topology
try:
    if hasattr(meraki.dashboard.networks, 'getNetworkTopologyLinkLayer'):
        result = meraki.dashboard.networks.getNetworkTopologyLinkLayer(network_id)
        print(f"✅ getNetworkTopologyLinkLayer works! Keys: {list(result.keys())}")
except Exception as e:
    print(f"❌ Network topology error: {e}")

# Try LLDP/CDP
try:
    if hasattr(meraki.dashboard.devices, 'getDeviceLldpCdp'):
        result = meraki.dashboard.devices.getDeviceLldpCdp(device_serial)
        print(f"✅ getDeviceLldpCdp works! Keys: {list(result.keys())}")
except Exception as e:
    print(f"❌ LLDP/CDP error: {e}")
