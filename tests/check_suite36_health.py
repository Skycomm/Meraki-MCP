#!/usr/bin/env python3
"""
Suite 36 - Hollywood Network Health Check
Matches the Meraki dashboard view
"""

from meraki_client import MerakiClient
from datetime import datetime
import time

# Suite 36 details
SUITE36_ORG_ID = '669347494617940173'
SUITE36_NETWORK_ID = 'L_669347494617955079'
SUITE36_MX_SERIAL = 'Q2MN-J5Y8-6L66'

def check_network_health():
    """Run comprehensive health check matching dashboard metrics."""
    meraki = MerakiClient()
    
    print('🏥 SUITE 36 - HOLLYWOOD HEALTH CHECK')
    print('=' * 70)
    print(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    # 1. Check current packet loss (5 min window)
    print('📊 Checking Packet Loss & Latency...')
    try:
        loss_data = meraki.get_organization_devices_uplinks_loss_and_latency(
            SUITE36_ORG_ID, 
            timespan=300
        )
        
        issues_found = False
        
        for device in loss_data:
            if device.get('serial') == SUITE36_MX_SERIAL:
                for uplink in device.get('uplinks', []):
                    if uplink.get('interface') == 'wan1':
                        time_series = uplink.get('timeSeries', [])
                        
                        if time_series:
                            # Get latest values
                            latest = time_series[-1]
                            current_loss = latest.get('lossPercent', 0)
                            current_latency = latest.get('latencyMs', 0)
                            
                            # Calculate 5-min averages
                            losses = [p.get('lossPercent', 0) for p in time_series if p.get('lossPercent') is not None]
                            latencies = [p.get('latencyMs', 0) for p in time_series if p.get('latencyMs') is not None]
                            
                            avg_loss = sum(losses) / len(losses) if losses else 0
                            avg_latency = sum(latencies) / len(latencies) if latencies else 0
                            
                            # Display results
                            print(f'\n✅ WAN1 Status ({uplink.get("ip")}):')
                            print(f'   Current: {current_loss:.1f}% loss, {current_latency:.0f}ms latency')
                            print(f'   5-min avg: {avg_loss:.1f}% loss, {avg_latency:.0f}ms latency')
                            
                            # Check thresholds
                            if current_loss > 1:
                                print(f'   ⚠️ WARNING: Packet loss detected!')
                                issues_found = True
                            
                            if current_latency > 100:
                                print(f'   ⚠️ WARNING: High latency!')
                                issues_found = True
                                
                            # Historical pattern notice
                            current_hour = datetime.now().hour
                            if 22 <= current_hour or current_hour <= 3:
                                print(f'   📌 Note: Dashboard shows typical loss during 10PM-3AM')
                            elif 12 <= current_hour <= 14:
                                print(f'   📌 Note: Dashboard shows typical loss during 12PM-2PM')
                                
    except Exception as e:
        print(f'❌ Error checking loss/latency: {e}')
    
    # 2. Check traffic levels
    print('\n\n📈 Checking Traffic Levels...')
    try:
        history = meraki.get_network_appliance_uplinks_usage_history(
            SUITE36_NETWORK_ID, 
            timespan=300  # Last 5 minutes
        )
        
        if history:
            total_kb = 0
            count = 0
            
            for entry in history[-5:]:  # Last 5 data points
                interfaces = entry.get('byInterface', [])
                for iface in interfaces:
                    if iface.get('interface') == 'wan1':
                        sent = iface.get('sent', 0)
                        received = iface.get('received', 0)
                        total_kb += (sent + received) / 1024
                        count += 1
            
            if count > 0:
                avg_kb = total_kb / count
                print(f'   Average traffic: {avg_kb:.1f} KB/minute')
                
                if avg_kb > 50000:  # 50 MB/min
                    print(f'   ⚠️ WARNING: Very high traffic usage!')
                    issues_found = True
                    
    except Exception as e:
        print(f'❌ Error checking traffic: {e}')
    
    # 3. Run ping tests
    print('\n\n🏓 Running Connectivity Tests...')
    targets = [
        ('8.8.8.8', 'Google DNS'),
        ('1.1.1.1', 'Cloudflare DNS')
    ]
    
    ping_ids = []
    for target, desc in targets:
        try:
            result = meraki.create_device_live_tools_ping(
                SUITE36_MX_SERIAL,
                target=target,
                count=3
            )
            if result and result.get('pingId'):
                ping_ids.append((result['pingId'], target, desc))
                print(f'   ✅ Testing {desc}...')
        except Exception as e:
            print(f'   ❌ Failed to test {desc}: {e}')
    
    # Wait for tests
    if ping_ids:
        print('   ⏳ Waiting for results...')
        time.sleep(10)
        
        for ping_id, target, desc in ping_ids:
            try:
                result = meraki.get_device_live_tools_ping(SUITE36_MX_SERIAL, ping_id)
                if result and result.get('results'):
                    results = result['results']
                    loss = results.get('loss', {}).get('percentage', 100)
                    
                    if loss > 0:
                        print(f'   ⚠️ {desc}: {loss:.0f}% packet loss')
                        issues_found = True
                    else:
                        print(f'   ✅ {desc}: No packet loss')
                        
            except Exception as e:
                print(f'   ❌ Error getting {desc} results: {e}')
    
    # Summary
    print('\n\n' + '=' * 70)
    if issues_found:
        print('⚠️ ISSUES DETECTED - Network performance degraded')
        print('\nRecommended Actions:')
        print('1. Check ISP status page')
        print('2. Verify cable connections')
        print('3. Review bandwidth usage')
        print('4. Monitor for patterns')
    else:
        print('✅ NETWORK HEALTHY - All metrics within normal range')
        print('\nYour dashboard shows historical packet loss during:')
        print('- 10PM-3AM (late night)')
        print('- 12PM-2PM (lunch hours)')
        print('This may be ISP maintenance or congestion.')

if __name__ == '__main__':
    check_network_health()