#!/usr/bin/env python3
"""
Test script to verify the extended coverage implementations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.main import app, meraki

def count_tools_in_module(module_name):
    """Count tools registered by a specific module."""
    count = 0
    for tool in app._tools.values():
        # Check if tool was registered by this module
        if hasattr(tool, '__module__') and module_name in tool.__module__:
            count += 1
    return count

def test_extended_coverage():
    """Test the new extended coverage modules."""
    
    print("=" * 60)
    print("TESTING EXTENDED COVERAGE IMPLEMENTATIONS")
    print("=" * 60)
    
    # Test Organizations Extended
    print("\n📋 Organizations Extended Module:")
    try:
        from server.tools_organizations_extended import register_organizations_extended_tools
        # Count tools with 'org' in name (organization tools)
        org_extended_tools = [name for name in app._tools.keys() if 'org_' in name and 'early' not in name]
        print(f"  ✅ Organizations extended tools registered: {len(org_extended_tools)}")
        
        # Sample some key tools
        key_org_tools = [
            'get_org_inventory_devices',
            'claim_org_devices', 
            'get_org_config_templates',
            'get_org_saml',
            'get_org_api_requests',
            'get_org_branding_policies',
            'get_org_login_security',
            'get_org_snmp',
            'get_org_action_batches',
            'get_org_adaptive_policy_acls',
            'get_org_summary_metrics',
            'clone_organization'
        ]
        
        missing_org = []
        for tool in key_org_tools:
            if tool in app._tools:
                print(f"    ✓ {tool}")
            else:
                missing_org.append(tool)
                print(f"    ✗ {tool} - MISSING")
                
        if missing_org:
            print(f"  ⚠️ Missing {len(missing_org)} organization tools")
    except Exception as e:
        print(f"  ❌ Error loading organizations extended: {e}")
    
    # Test Networks Extended
    print("\n🌐 Networks Extended Module:")
    try:
        from server.tools_networks_extended import register_networks_extended_tools
        # Count network extended tools
        net_extended_tools = [name for name in app._tools.keys() if 'network_' in name and 'wireless' not in name and 'camera' not in name]
        print(f"  ✅ Networks extended tools registered: {len(net_extended_tools)}")
        
        # Sample some key tools
        key_net_tools = [
            'get_network_alerts_history',
            'get_network_clients',
            'get_network_client_details',
            'get_network_firmware_upgrades',
            'get_network_floor_plans',
            'get_network_group_policies',
            'get_network_meraki_auth_users',
            'get_network_pii_requests',
            'get_network_traffic_analysis',
            'get_network_traffic_shaping'
        ]
        
        missing_net = []
        for tool in key_net_tools:
            if tool in app._tools:
                print(f"    ✓ {tool}")
            else:
                missing_net.append(tool)
                print(f"    ✗ {tool} - MISSING")
                
        if missing_net:
            print(f"  ⚠️ Missing {len(missing_net)} network tools")
    except Exception as e:
        print(f"  ❌ Error loading networks extended: {e}")
    
    # Test Camera Updates
    print("\n📸 Camera Module (Updated):")
    camera_tools = [name for name in app._tools.keys() if 'camera' in name]
    print(f"  ✅ Camera tools registered: {len(camera_tools)}")
    
    key_camera_tools = [
        'get_device_camera_video_link',
        'get_device_camera_snapshot',
        'get_device_camera_video_settings',
        'get_device_camera_analytics_zones',
        'get_device_camera_sense',
        'update_device_camera_sense',
        'get_device_camera_custom_analytics',
        'get_network_camera_schedules',
        'get_network_camera_quality_profiles',
        'get_network_camera_wireless_profiles',
        'get_org_camera_boundaries_lines',
        'get_org_camera_detections_history'
    ]
    
    missing_camera = []
    for tool in key_camera_tools:
        if tool in app._tools:
            print(f"    ✓ {tool}")
        else:
            missing_camera.append(tool)
            print(f"    ✗ {tool} - MISSING")
            
    if missing_camera:
        print(f"  ⚠️ Missing {len(missing_camera)} camera tools")
    
    # Overall Summary
    print("\n" + "=" * 60)
    print("COVERAGE SUMMARY")
    print("=" * 60)
    
    total_tools = len(app._tools)
    print(f"\n📊 Total MCP Tools: {total_tools}")
    
    # Count by category
    categories = {
        'Organizations': len([n for n in app._tools.keys() if 'org' in n or 'organization' in n]),
        'Networks': len([n for n in app._tools.keys() if 'network' in n and 'wireless' not in n and 'camera' not in n]),
        'Wireless': len([n for n in app._tools.keys() if 'wireless' in n]),
        'Camera': len([n for n in app._tools.keys() if 'camera' in n]),
        'Devices': len([n for n in app._tools.keys() if 'device' in n and 'camera' not in n]),
        'Switch': len([n for n in app._tools.keys() if 'switch' in n]),
        'Appliance': len([n for n in app._tools.keys() if 'appliance' in n]),
        'SM': len([n for n in app._tools.keys() if 'sm_' in n]),
        'Sensor': len([n for n in app._tools.keys() if 'sensor' in n]),
        'Cellular': len([n for n in app._tools.keys() if 'cellular' in n])
    }
    
    print("\nTools by Category:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat:15} : {count:3} tools")
    
    # Check parameter consistency
    print("\n🔍 Parameter Consistency Check:")
    param_patterns = {
        'organization_id': 0,
        'network_id': 0,
        'serial': 0,
        'device_serial': 0,
        'confirmed': 0,
        'per_page': 0,
        'timespan': 0
    }
    
    for tool_name, tool_func in app._tools.items():
        if hasattr(tool_func, '__code__'):
            params = tool_func.__code__.co_varnames[:tool_func.__code__.co_argcount]
            for param in params:
                if param in param_patterns:
                    param_patterns[param] += 1
    
    print("  Common parameter usage:")
    for param, count in sorted(param_patterns.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"    {param:20} : {count:3} occurrences")
    
    print("\n✅ Extended coverage test complete!")
    
    return total_tools

if __name__ == "__main__":
    try:
        total = test_extended_coverage()
        print(f"\n🎉 Successfully loaded {total} total tools!")
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()