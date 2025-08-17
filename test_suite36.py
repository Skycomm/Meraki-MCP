#!/usr/bin/env python3
"""
Test script for Suite 36 - Hollywood network issues.
"""

from meraki_client import MerakiClient

# Initialize client
meraki = MerakiClient()

# Suite 36 details from the test
SUITE36_ORG_ID = "669347494617940173"
SUITE36_NETWORK_ID = "L_669347494617955079"
SUITE36_MX_SERIAL = "Q2MN-J5Y8-6L66"

print("🧪 Testing Suite 36 - Hollywood Network")
print("=" * 60)

# 1. Test organization access
print("\n1. Testing organization access...")
try:
    orgs = meraki.get_organizations()
    print(f"✅ Found {len(orgs)} organizations")
    
    # Find Suite 36 org
    suite36_org = None
    for org in orgs:
        if org.get('id') == SUITE36_ORG_ID:
            suite36_org = org
            print(f"✅ Found organization: {org.get('name')} (ID: {org.get('id')})")
            break
    
    if not suite36_org:
        print(f"❌ Organization {SUITE36_ORG_ID} not found in accessible orgs")
        print("Available organizations:")
        for org in orgs[:5]:  # Show first 5
            print(f"  - {org.get('name')} (ID: {org.get('id')})")
except Exception as e:
    print(f"❌ Error accessing organizations: {e}")

# 2. Test uplink loss/latency with proper timespan
print("\n2. Testing uplink loss/latency...")
try:
    # Test with 300 second timespan (max allowed)
    result = meraki.get_organization_devices_uplinks_loss_and_latency(SUITE36_ORG_ID, timespan=300)
    if result:
        print(f"✅ Got uplink data for {len(result)} devices")
        
        # Look for Suite 36 MX
        for device in result:
            if device.get('serial') == SUITE36_MX_SERIAL:
                print(f"\n📊 Suite 36 MX64W Uplink Status:")
                print(f"   Serial: {device.get('serial')}")
                print(f"   Network: {device.get('networkId')}")
                
                # Check uplinks
                uplinks = device.get('uplinks', [])
                for uplink in uplinks:
                    print(f"\n   Uplink: {uplink.get('interface', 'Unknown')}")
                    print(f"   IP: {uplink.get('ip', 'N/A')}")
                    
                    # Get latest data
                    timeSeries = uplink.get('timeSeries', [])
                    if timeSeries:
                        latest = timeSeries[-1]
                        loss = latest.get('lossPercent', 0)
                        latency = latest.get('latencyMs', 0)
                        
                        print(f"   Packet Loss: {loss}%")
                        print(f"   Latency: {latency}ms")
                        
                        if loss > 1:
                            print("   ⚠️ WARNING: Packet loss detected!")
                        if latency > 100:
                            print("   ⚠️ WARNING: High latency detected!")
    else:
        print("⚠️ No uplink data returned")
        
except Exception as e:
    print(f"❌ Error getting uplink data: {e}")

# 3. Test network-specific stats
print("\n3. Testing network connection stats...")
try:
    conn_stats = meraki.get_network_connection_stats(SUITE36_NETWORK_ID, timespan=300)
    if conn_stats:
        print("✅ Got connection statistics")
        
        # Check for issues
        assoc_stats = conn_stats.get('assoc', 0)
        auth_stats = conn_stats.get('auth', 0) 
        dhcp_stats = conn_stats.get('dhcp', 0)
        dns_stats = conn_stats.get('dns', 0)
        success_stats = conn_stats.get('success', 0)
        
        print(f"   Association: {assoc_stats}")
        print(f"   Authentication: {auth_stats}")
        print(f"   DHCP: {dhcp_stats}")
        print(f"   DNS: {dns_stats}")
        print(f"   Success: {success_stats}")
        
except Exception as e:
    print(f"❌ Error getting connection stats: {e}")

# 4. Test latency stats
print("\n4. Testing network latency...")
try:
    latency_stats = meraki.get_network_latency_stats(SUITE36_NETWORK_ID, timespan=300)
    if latency_stats:
        print("✅ Got latency statistics")
        
        # Background traffic
        bg_traffic = latency_stats.get('backgroundTraffic', {})
        if bg_traffic:
            raw_dist = bg_traffic.get('rawDistribution', {})
            if raw_dist:
                print("\n   Background Traffic Latency Distribution:")
                for bucket, count in raw_dist.items():
                    if count > 0:
                        print(f"   {bucket}: {count} samples")
                        
except Exception as e:
    print(f"❌ Error getting latency stats: {e}")

# 5. Test live ping FROM the MX
print("\n5. Testing live ping from MX...")
try:
    ping_test = meraki.create_device_live_tools_ping(
        SUITE36_MX_SERIAL,
        target="8.8.8.8",
        count=5
    )
    if ping_test:
        print(f"✅ Ping test created with ID: {ping_test.get('id')}")
        print("   (Wait a few seconds then retrieve results with get_device_ping_test)")
except Exception as e:
    print(f"❌ Error creating ping test: {e}")

print("\n" + "="*60)
print("Suite 36 testing complete!")
print("\nRecommendations:")
print("1. Check if organization ID is correct")
print("2. Verify API key has access to this organization") 
print("3. Use timespan <= 300 for uplink API")
print("4. Test with live tools for real-time diagnostics")