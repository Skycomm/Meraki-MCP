#!/usr/bin/env python3
"""
Diagnose client count history API issues
"""

from meraki_client import MerakiClient
from datetime import datetime, timedelta
import json

# Initialize client
meraki = MerakiClient()

# Network and org IDs
network_id = 'L_726205439913500692'
org_id = '686470'

print("🔍 Diagnosing Client Count History API Issues\n")

# 1. Check Early Access status
print("1️⃣ Checking Early Access Status...")
try:
    opt_ins = meraki.get_organization_early_access_features_opt_ins(org_id)
    if opt_ins:
        print(f"✅ Early Access Features Enabled: {len(opt_ins)}")
        for opt_in in opt_ins:
            print(f"   - {opt_in.get('shortName', 'Unknown')}")
    else:
        print("❌ No Early Access features enabled")
        print("   💡 Some wireless analytics features may require Early Access")
except Exception as e:
    print(f"⚠️ Could not check Early Access: {e}")

print("\n2️⃣ Testing Client Count History API...")

# Test different time ranges and resolutions
test_configs = [
    {"timespan": 300, "resolution": 60, "desc": "5 minutes, 1-minute resolution"},
    {"timespan": 3600, "resolution": 300, "desc": "1 hour, 5-minute resolution"},
    {"timespan": 86400, "resolution": 3600, "desc": "24 hours, 1-hour resolution"},
    {"timespan": 604800, "resolution": 86400, "desc": "7 days, daily resolution"},
]

for config in test_configs:
    print(f"\n📊 Testing: {config['desc']}")
    try:
        history = meraki.get_network_wireless_client_count_history(
            network_id, 
            timespan=config['timespan'],
            resolution=config['resolution']
        )
        
        if history:
            print(f"   ✅ Got {len(history)} data points")
            if len(history) > 0:
                first = history[0]
                last = history[-1]
                print(f"   📅 From: {first.get('startTs', 'Unknown')}")
                print(f"   📅 To: {last.get('endTs', 'Unknown')}")
                
                # Show client count range
                counts = [h.get('clientCount', 0) for h in history]
                print(f"   👥 Client range: {min(counts)} - {max(counts)}")
        else:
            print("   ❌ No data returned")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

# 3. Test per-device data
print("\n3️⃣ Testing Per-Device Client History...")
try:
    devices = meraki.get_network_devices(network_id)
    aps = [d for d in devices if d.get('model', '').startswith('MR')]
    
    for ap in aps[:2]:  # Test first 2 APs
        print(f"\n📡 {ap.get('name', 'Unnamed')} ({ap['serial']})")
        try:
            history = meraki.get_network_wireless_client_count_history(
                network_id,
                timespan=3600,
                device_serial=ap['serial'],
                resolution=300
            )
            if history:
                print(f"   ✅ Got {len(history)} data points")
            else:
                print("   ❌ No data")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
except Exception as e:
    print(f"❌ Could not get devices: {e}")

# 4. Test band-specific data
print("\n4️⃣ Testing Band-Specific History...")
for band in ['2.4', '5']:
    print(f"\n📻 {band} GHz Band")
    try:
        history = meraki.get_network_wireless_client_count_history(
            network_id,
            timespan=3600,
            band=band,
            resolution=300
        )
        if history:
            print(f"   ✅ Got {len(history)} data points")
            counts = [h.get('clientCount', 0) for h in history]
            print(f"   👥 Average: {sum(counts)/len(counts):.1f} clients")
        else:
            print("   ❌ No data")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# 5. Alternative: Check current client count
print("\n5️⃣ Current Client Count (for comparison)...")
try:
    clients = meraki.get_network_clients(network_id, timespan=300)
    print(f"✅ Current clients: {len(clients)}")
    
    # Count by device
    by_device = {}
    for client in clients:
        device = client.get('recentDeviceName', 'Unknown')
        by_device[device] = by_device.get(device, 0) + 1
    
    for device, count in sorted(by_device.items(), key=lambda x: x[1], reverse=True):
        print(f"   {device}: {count} clients")
        
except Exception as e:
    print(f"❌ Error getting current clients: {e}")

print("\n📝 Summary:")
print("If client count history returns limited data, it could be due to:")
print("1. Data retention limits on the Meraki platform")
print("2. Network type or licensing limitations")
print("3. Need for specific Early Access features")
print("4. API endpoint still being in development/beta")
print("\n💡 Recommendation: Use current client snapshots with external")
print("   time-series storage for long-term trending if needed.")