from meraki_client import MerakiClient

# Initialize the client
meraki = MerakiClient()

network_id = 'L_726205439913500692'

print('Checking for critical alerts and issues in Reserve St network...')
print('=' * 60)

# 1. Check device statuses
print('\n1. Device Status Check:')
print('-' * 40)
try:
    devices = meraki.dashboard.networks.getNetworkDevices(network_id)
    org_id = '686470'  # Skycomm org ID
    
    # Get organization device statuses
    statuses = meraki.dashboard.organizations.getOrganizationDevicesStatuses(
        org_id,
        networkIds=[network_id]
    )
    
    status_map = {s['serial']: s for s in statuses}
    
    for device in devices:
        serial = device['serial']
        status_info = status_map.get(serial, {})
        status = status_info.get('status', 'unknown')
        
        if status != 'online':
            print(f"  🔴 {device.get('name', serial)} ({device['model']}): {status.upper()}")
            if status_info.get('lastReportedAt'):
                print(f"     Last seen: {status_info['lastReportedAt']}")
        else:
            print(f"  ✅ {device.get('name', serial)} ({device['model']}): Online")
            
except Exception as e:
    print(f"  Error checking device status: {e}")

# 2. Check uplink status for MX
print('\n2. Uplink Status Check:')
print('-' * 40)
try:
    uplinks = meraki.dashboard.appliance.getNetworkApplianceUplinksSettings(network_id)
    print(f"  WAN 1: {uplinks.get('wan1', {}).get('enabled', 'Unknown')}")
    print(f"  WAN 2: {uplinks.get('wan2', {}).get('enabled', 'Unknown')}")
    
    # Get uplink status
    uplink_statuses = meraki.dashboard.organizations.getOrganizationApplianceUplinkStatuses(org_id)
    
    for status in uplink_statuses:
        if status.get('networkId') == network_id:
            for uplink in status.get('uplinks', []):
                interface = uplink.get('interface', 'Unknown')
                state = uplink.get('status', 'Unknown')
                ip = uplink.get('ip', 'No IP')
                
                if state != 'active':
                    print(f"  🔴 {interface}: {state.upper()} ({ip})")
                else:
                    print(f"  ✅ {interface}: Active ({ip})")
                    
except Exception as e:
    print(f"  Error checking uplink status: {e}")

# 3. Check for wireless issues
print('\n3. Wireless Health Check:')
print('-' * 40)
try:
    # Get connection stats for last hour
    conn_stats = meraki.dashboard.networks.getNetworkConnectionStats(
        network_id,
        timespan=3600
    )
    
    if conn_stats:
        assoc = conn_stats.get('assoc', 0)
        auth = conn_stats.get('auth', 0)
        dhcp = conn_stats.get('dhcp', 0)
        dns = conn_stats.get('dns', 0)
        success = conn_stats.get('success', 0)
        
        total_attempts = assoc if assoc > 0 else 1
        success_rate = (success / total_attempts) * 100 if total_attempts > 0 else 0
        
        print(f"  Connection Success Rate: {success_rate:.1f}%")
        
        if success_rate < 80:
            print(f"  🔴 LOW SUCCESS RATE - Potential issues detected")
            if auth < assoc * 0.9:
                print(f"     - Authentication failures: {assoc - auth} of {assoc} attempts")
            if dhcp < auth * 0.9:
                print(f"     - DHCP failures: {auth - dhcp} of {auth} authenticated")
            if dns < dhcp * 0.9:
                print(f"     - DNS failures: {dhcp - dns} of {dhcp} with DHCP")
        else:
            print(f"  ✅ Connection health is good")
            
except Exception as e:
    print(f"  Error checking wireless health: {e}")

# 4. Check for recent security events  
print('\n4. Security Event Check:')
print('-' * 40)
try:
    # Try to get security events
    sec_events = meraki.dashboard.appliance.getNetworkApplianceSecurityEvents(
        network_id,
        timespan=86400  # 24 hours
    )
    
    if sec_events:
        print(f"  Found {len(sec_events)} security events")
        # Show first 5
        for event in sec_events[:5]:
            print(f"  - {event.get('message', 'No message')} at {event.get('ts', 'Unknown time')}")
    else:
        print("  ✅ No security events in last 24 hours")
        
except Exception as e:
    print(f"  No security events or not applicable: {str(e)}")

# 5. Summary
print('\n' + '=' * 60)
print('\nSUMMARY:')

# The 1000 disassociation events from wireless are concerning
print('\n⚠️  KEY FINDINGS:')
print('  - 1000+ wireless disassociation events in 24 hours')
print('  - This indicates potential wireless stability issues')
print('  - Could be caused by:')
print('    • Interference or poor signal')
print('    • Client roaming between APs')
print('    • Authentication/configuration issues')
print('    • Power save mode on clients')

print('\n💡 RECOMMENDATIONS:')
print('  1. Check wireless signal strength and coverage')
print('  2. Review AP placement and channel settings')
print('  3. Check for interference sources')
print('  4. Review client device settings')
print('  5. Consider enabling band steering if not already enabled')