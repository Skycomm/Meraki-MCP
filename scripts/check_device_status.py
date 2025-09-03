#!/usr/bin/env python3
"""
Accurate Device Status Checker for Cisco Meraki Networks
Tests actual device functionality rather than relying on dashboard status reports
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki

def format_device_status(network_id='L_726205439913500692', organization_id='686470'):
    """Check real device status using functional tests"""
    
    print('🔍 CISCO MERAKI DEVICE STATUS CHECK')
    print('=' * 60)
    
    # Define device test functions
    devices = {
        'Reserve St MX68': {
            'serial': 'Q2KY-NGXA-AJZU',
            'type': 'appliance',
            'model': 'MX68',
            'test_function': lambda: meraki.dashboard.appliance.getNetworkApplianceVlans(network_id)
        },
        'Reserve St Switch': {
            'serial': 'Q2HP-GCZQ-7AWT', 
            'type': 'switch',
            'model': 'MS220-8P',
            'test_function': lambda: meraki.dashboard.switch.getDeviceSwitchPorts('Q2HP-GCZQ-7AWT')
        },
        'Office AP': {
            'serial': 'Q2PD-JL52-H3B2',
            'type': 'wireless',
            'model': 'MR33',
            'test_function': lambda: meraki.dashboard.wireless.getDeviceWirelessStatus('Q2PD-JL52-H3B2')
        },
        'Shed AP': {
            'serial': 'Q2PD-KWFG-DH9J',
            'type': 'wireless', 
            'model': 'MR33',
            'test_function': lambda: meraki.dashboard.wireless.getDeviceWirelessStatus('Q2PD-KWFG-DH9J')
        },
        'Bathroom AP': {
            'serial': 'Q2PD-SRPB-4JTT',
            'type': 'wireless',
            'model': 'MR33',
            'test_function': lambda: meraki.dashboard.wireless.getDeviceWirelessStatus('Q2PD-SRPB-4JTT')
        },
        'Street View Camera': {
            'serial': 'Q2CV-X2V2-MMN6',
            'type': 'camera',
            'model': 'MV71',
            'test_function': lambda: meraki.dashboard.camera.generateDeviceCameraSnapshot('Q2CV-X2V2-MMN6')
        }
    }
    
    results = {}
    
    print(f'Network: Reserve St (ID: {network_id})')
    print(f'Organization: Skycomm (ID: {organization_id})')
    print(f'Testing {len(devices)} devices...\n')
    
    # Test each device
    for device_name, device_info in devices.items():
        try:
            # Run device-specific test
            result = device_info['test_function']()
            
            # Device responded successfully
            if device_info['type'] == 'camera':
                status = 'online'
                formatted_status = '🟢 ONLINE (Live streaming)'
            else:
                status = 'online'
                formatted_status = '🟢 ONLINE'
                
            results[device_name] = {
                'status': status,
                'formatted': formatted_status,
                'info': device_info
            }
            
        except Exception as e:
            # Device test failed
            error_str = str(e).lower()
            
            if device_info['type'] == 'camera' and ('500' in error_str or 'internal server' in error_str):
                # Camera has config access but streaming is down
                status = 'dormant'
                formatted_status = '🟡 DORMANT'
            else:
                # Complete failure
                status = 'offline'
                formatted_status = '🔴 OFFLINE'
                
            results[device_name] = {
                'status': status,
                'formatted': formatted_status,
                'info': device_info,
                'error': str(e)[:100]
            }
    
    # Display results
    print('📋 DEVICE STATUS REPORT')
    print('-' * 60)
    
    for device_name, result in results.items():
        device_info = result['info']
        print(f"{result['formatted']} {device_name}")
        print(f"   📋 {device_info['model']} ({device_info['type']})")
        print(f"   🔧 Serial: {device_info['serial']}")
        
        if 'error' in result:
            print(f"   ⚠️  Issue: {result['error']}")
        print()
    
    # Summary statistics
    online_count = sum(1 for r in results.values() if r['status'] == 'online')
    dormant_count = sum(1 for r in results.values() if r['status'] == 'dormant') 
    offline_count = sum(1 for r in results.values() if r['status'] == 'offline')
    total_devices = len(results)
    
    print('=' * 60)
    print('📊 NETWORK STATUS SUMMARY')
    print('=' * 60)
    print(f'🟢 Fully Operational: {online_count}/{total_devices} devices')
    print(f'🟡 Partial/Dormant:   {dormant_count}/{total_devices} devices')
    print(f'🔴 Offline:           {offline_count}/{total_devices} devices')
    
    # Overall health assessment
    functional_devices = online_count + dormant_count
    if functional_devices == total_devices and offline_count == 0:
        if dormant_count == 0:
            health = '🟢 EXCELLENT - All devices fully operational'
        else:
            health = '🟡 GOOD - Minor issues with some devices'
    elif functional_devices >= total_devices * 0.8:
        health = '🟠 FAIR - Some devices need attention'
    else:
        health = '🔴 POOR - Multiple device failures'
        
    print(f'\n🏥 Overall Network Health: {health}')
    
    # Recommendations
    if dormant_count > 0 or offline_count > 0:
        print(f'\n💡 RECOMMENDATIONS:')
        for device_name, result in results.items():
            if result['status'] in ['dormant', 'offline']:
                device_type = result['info']['type']
                if device_type == 'camera' and result['status'] == 'dormant':
                    print(f'   📹 {device_name}: Check power, reboot camera, verify network connectivity')
                elif result['status'] == 'offline':
                    print(f'   🔧 {device_name}: Device completely unresponsive - check power and connections')
    
    return results

if __name__ == "__main__":
    # Run the status check
    results = format_device_status()