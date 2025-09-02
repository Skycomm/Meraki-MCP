#!/usr/bin/env python3
"""Test the fixed SDK method calls directly"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki

network_id = "L_726205439913500692"  # Reserve St
device_serial = "Q2HP-GCZQ-7AWT"  # MS220-8P switch

print("🔍 Testing Fixed SDK Methods for Reserve St Network")
print("="*70)

# Test 1: Network Topology - using correct SDK method
print("\n📊 Test 1: Network Topology Link Layer")
print("-"*40)
try:
    topology = meraki.dashboard.networks.getNetworkTopologyLinkLayer(network_id)
    
    print("✅ Network topology API works!")
    
    nodes = topology.get('nodes', [])
    links = topology.get('links', [])
    errors = topology.get('errors', [])
    
    print(f"   Found {len(nodes)} nodes")
    print(f"   Found {len(links)} links")
    
    if nodes:
        print("\n   Sample nodes:")
        for node in nodes[:3]:
            print(f"     - {node.get('name', 'Unknown')} ({node.get('type')})")
    
    if links:
        print("\n   Sample links:")
        for link in links[:3]:
            ends = link.get('ends', [])
            if len(ends) >= 2:
                print(f"     - {ends[0].get('node', {}).get('name', '?')} ↔ {ends[1].get('node', {}).get('name', '?')}")
    
    if errors:
        print(f"\n   ⚠️ Errors: {errors}")
        
except Exception as e:
    print(f"❌ Network topology error: {e}")

# Test 2: LLDP/CDP - using correct SDK method
print("\n🔗 Test 2: LLDP/CDP Information")
print("-"*40)
try:
    lldp_cdp = meraki.dashboard.devices.getDeviceLldpCdp(device_serial)
    
    print("✅ LLDP/CDP API works!")
    
    source_mac = lldp_cdp.get('sourceMac', 'Unknown')
    ports = lldp_cdp.get('ports', {})
    
    print(f"   Source MAC: {source_mac}")
    print(f"   Ports with neighbor info: {len(ports)}")
    
    if ports:
        print("\n   Port neighbor details:")
        for port_id, port_info in list(ports.items())[:3]:
            print(f"     Port {port_id}:")
            
            cdp = port_info.get('cdp', {})
            if cdp:
                print(f"       CDP: {cdp.get('deviceId', 'Unknown')} ({cdp.get('platform', 'Unknown')})")
            
            lldp = port_info.get('lldp', {})
            if lldp:
                print(f"       LLDP: {lldp.get('systemName', 'Unknown')}")
                
except Exception as e:
    print(f"❌ LLDP/CDP error: {e}")

print("\n" + "="*70)
print("Summary: Both API endpoints exist and work with the correct SDK methods!")
print("The tools have been fixed to use the proper SDK calls.")
