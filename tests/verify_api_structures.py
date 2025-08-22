#!/usr/bin/env python3
"""
Verify ALL API data structures to ensure correct parsing
"""

from meraki_client import MerakiClient
import json
from typing import Any, Dict

def check_data_structure(api_name: str, data: Any, expected_type: type = None) -> bool:
    """Check if API response matches expected structure."""
    print(f"\n{'='*60}")
    print(f"API: {api_name}")
    print(f"Type: {type(data)}")
    
    if expected_type and not isinstance(data, expected_type):
        print(f"❌ WRONG TYPE! Expected {expected_type}, got {type(data)}")
        return False
    
    # Show structure
    if isinstance(data, list) and len(data) > 0:
        print(f"List length: {len(data)}")
        print(f"First item type: {type(data[0])}")
        if isinstance(data[0], dict):
            print(f"First item keys: {list(data[0].keys())}")
            # Show sample
            print(f"Sample: {json.dumps(data[0], indent=2)[:200]}...")
    elif isinstance(data, dict):
        print(f"Dict keys: {list(data.keys())}")
        print(f"Sample: {json.dumps(data, indent=2)[:200]}...")
    else:
        print(f"Value: {data}")
    
    return True

def main():
    meraki = MerakiClient()
    
    # Test org and network IDs
    TEST_ORG_ID = '669347494617940173'  # JMLS
    TEST_NETWORK_ID = 'L_669347494617955079'  # Suite 36
    TEST_MX_SERIAL = 'Q2MN-J5Y8-6L66'
    
    print("🔍 VERIFYING ALL API DATA STRUCTURES")
    print("="*80)
    
    errors = []
    
    # 1. Organization APIs
    print("\n📁 ORGANIZATION APIs")
    
    try:
        orgs = meraki.get_organizations()
        if not check_data_structure("get_organizations", orgs, list):
            errors.append("get_organizations returns wrong type")
    except Exception as e:
        errors.append(f"get_organizations: {e}")
    
    try:
        org = meraki.get_organization(TEST_ORG_ID)
        if not check_data_structure("get_organization", org, dict):
            errors.append("get_organization returns wrong type")
    except Exception as e:
        errors.append(f"get_organization: {e}")
    
    # 2. Device APIs
    print("\n\n📱 DEVICE APIs")
    
    try:
        devices = meraki.get_organization_devices(TEST_ORG_ID)
        if not check_data_structure("get_organization_devices", devices, list):
            errors.append("get_organization_devices returns wrong type")
    except Exception as e:
        errors.append(f"get_organization_devices: {e}")
    
    try:
        device = meraki.get_device(TEST_MX_SERIAL)
        if not check_data_structure("get_device", device, dict):
            errors.append("get_device returns wrong type")
    except Exception as e:
        errors.append(f"get_device: {e}")
    
    # 3. Analytics APIs (CRITICAL ONES)
    print("\n\n📊 ANALYTICS APIs (Critical)")
    
    try:
        loss_latency = meraki.get_organization_devices_uplinks_loss_and_latency(TEST_ORG_ID, timespan=300)
        check = check_data_structure("get_organization_devices_uplinks_loss_and_latency", loss_latency, list)
        
        # Check nested structure
        if check and len(loss_latency) > 0:
            for device in loss_latency:
                if device.get('serial') == TEST_MX_SERIAL:
                    print(f"\n  Found MX device data:")
                    print(f"  Device keys: {list(device.keys())}")
                    
                    uplinks = device.get('uplinks', [])
                    if uplinks and len(uplinks) > 0:
                        print(f"  Uplink keys: {list(uplinks[0].keys())}")
                        
                        # Check timeSeries structure
                        ts = uplinks[0].get('timeSeries', [])
                        if ts and len(ts) > 0:
                            print(f"  TimeSeries entry keys: {list(ts[0].keys())}")
                            print(f"  Sample: {ts[0]}")
                    break
                    
    except Exception as e:
        errors.append(f"get_organization_devices_uplinks_loss_and_latency: {e}")
    
    try:
        uplink_history = meraki.get_network_appliance_uplinks_usage_history(TEST_NETWORK_ID, timespan=3600)
        check = check_data_structure("get_network_appliance_uplinks_usage_history", uplink_history, list)
        
        # Verify byInterface structure
        if check and len(uplink_history) > 0:
            entry = uplink_history[0]
            if 'byInterface' in entry:
                print(f"\n  byInterface type: {type(entry['byInterface'])}")
                if isinstance(entry['byInterface'], list) and len(entry['byInterface']) > 0:
                    print(f"  Interface entry: {entry['byInterface'][0]}")
                    
    except Exception as e:
        errors.append(f"get_network_appliance_uplinks_usage_history: {e}")
    
    # 4. Live Tools APIs
    print("\n\n🔧 LIVE TOOLS APIs")
    
    try:
        # Create ping test
        ping_result = meraki.create_device_live_tools_ping(TEST_MX_SERIAL, target='8.8.8.8', count=1)
        check = check_data_structure("create_device_live_tools_ping", ping_result, dict)
        
        if check and 'pingId' in ping_result:
            import time
            time.sleep(5)
            
            # Get results
            ping_status = meraki.get_device_live_tools_ping(TEST_MX_SERIAL, ping_result['pingId'])
            check = check_data_structure("get_device_live_tools_ping", ping_status, dict)
            
            # Check results structure
            if check and 'results' in ping_status:
                print(f"\n  Results structure: {type(ping_status['results'])}")
                print(f"  Results keys: {list(ping_status['results'].keys())}")
                
    except Exception as e:
        errors.append(f"Live tools ping: {e}")
    
    # 5. Connection Stats
    print("\n\n📡 CONNECTION STATS")
    
    try:
        conn_stats = meraki.get_network_connection_stats(TEST_NETWORK_ID, timespan=300)
        check_data_structure("get_network_connection_stats", conn_stats)
        
        # This might be a dict or list depending on the API
        if isinstance(conn_stats, dict):
            print("  ⚠️ Returns dict - may need to handle differently")
        elif isinstance(conn_stats, list) and len(conn_stats) > 0:
            print(f"  Entry structure: {conn_stats[0]}")
            
    except Exception as e:
        errors.append(f"get_network_connection_stats: {e}")
    
    # 6. Performance API
    print("\n\n⚡ PERFORMANCE API")
    
    try:
        perf = meraki.get_device_appliance_performance(TEST_MX_SERIAL)
        check_data_structure("get_device_appliance_performance", perf, dict)
    except Exception as e:
        errors.append(f"get_device_appliance_performance: {e}")
    
    # Summary
    print("\n\n" + "="*80)
    print("📋 VERIFICATION SUMMARY")
    print("="*80)
    
    if errors:
        print(f"\n❌ Found {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        
        print("\n🔧 These need to be fixed in the MCP server!")
    else:
        print("\n✅ All API structures verified correctly!")
        
    print("\n📌 Key findings:")
    print("1. uplinks_usage_history: byInterface is a LIST, not dict")
    print("2. loss_and_latency: Returns list of devices with nested uplinks")
    print("3. ping results: Has 'results' dict with loss as nested object")
    print("4. connection_stats: May return dict or list - needs handling")

if __name__ == '__main__':
    main()