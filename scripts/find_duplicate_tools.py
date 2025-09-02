#!/usr/bin/env python3
"""
Find duplicate tool registrations between SDK and Custom modules.
SDK tools take precedence - mark custom duplicates for removal.
"""

def find_duplicate_tools():
    """Find duplicate tools based on startup warnings."""
    
    print("🔍 FINDING DUPLICATE TOOL REGISTRATIONS\n")
    
    # These are the duplicates found during startup
    duplicates = [
        'get_network_alerts_settings',
        'update_network_alerts_settings', 
        'get_organization_appliance_uplink_statuses',
        'get_organization_early_access_features',
        'get_organization_early_access_features_opt_ins',
        'create_device_live_tools_ping',
        'get_device_live_tools_ping', 
        'create_device_live_tools_ping_device',
        'get_device_live_tools_ping_device',
        'create_device_live_tools_cable_test',
        'get_device_live_tools_cable_test',
        'create_device_live_tools_wake_on_lan', 
        'get_device_live_tools_wake_on_lan',
        'create_device_live_tools_throughput_test',
        'get_device_live_tools_throughput_test', 
        'create_device_live_tools_arp_table',
        'get_device_live_tools_arp_table',
        'get_network_events',
        'get_organization_policy_objects',
        'create_organization_policy_object',
        'update_organization_policy_object',
        'delete_organization_policy_object', 
        'get_organization_policy_objects_groups',
        'create_organization_policy_objects_group',
        'update_organization_appliance_vpn_third_party_vpn_peers',
        'get_organization_appliance_vpn_statuses',
        'update_network_appliance_vpn_bgp',
        'update_organization_appliance_vpn_vpn_firewall_rules',
        'get_device_appliance_uplinks_settings', 
        'update_device_appliance_uplinks_settings'
    ]
    
    print(f"## 🎯 Found {len(duplicates)} duplicate tools\n")
    
    # Analyze which modules likely contain these
    module_mapping = {}
    
    for tool in duplicates:
        if 'network_alerts' in tool:
            module_mapping[tool] = {'sdk': 'networks', 'custom': 'alerts or wireless'}
        elif 'organization_appliance' in tool or 'device_appliance' in tool:
            module_mapping[tool] = {'sdk': 'appliance', 'custom': 'vpn or appliance'}
        elif 'organization_early_access' in tool:
            module_mapping[tool] = {'sdk': 'organizations', 'custom': 'organizations_custom'}
        elif 'device_live_tools' in tool:
            module_mapping[tool] = {'sdk': 'devices', 'custom': 'devices_custom or live_tools'}
        elif 'network_events' in tool:
            module_mapping[tool] = {'sdk': 'networks', 'custom': 'events or monitoring'}
        elif 'policy_object' in tool:
            module_mapping[tool] = {'sdk': 'organizations', 'custom': 'policy'}
        else:
            module_mapping[tool] = {'sdk': 'unknown', 'custom': 'unknown'}
    
    print("### 🔍 Analysis by Category:")
    
    categories = {}
    for tool, mapping in module_mapping.items():
        sdk_module = mapping['sdk']
        if sdk_module not in categories:
            categories[sdk_module] = []
        categories[sdk_module].append(tool)
    
    for sdk_module, tools in categories.items():
        print(f"\\n**{sdk_module.upper()} SDK Tools ({len(tools)} duplicates):**")
        for tool in tools[:5]:  # Show first 5
            print(f"   - {tool}")
        if len(tools) > 5:
            print(f"   ... and {len(tools)-5} more")
    
    print(f"\\n## 🧹 RECOMMENDED ACTION:")
    print(f"✅ **Keep**: All SDK module implementations (official API coverage)")
    print(f"🗑️ **Remove**: Custom module duplicates (redundant implementations)")
    print(f"🎯 **Priority**: Networks, Devices, Organizations, Appliance modules")
    
    print(f"\\n### 📋 Next Steps:")
    print(f"1. Disable duplicate custom tool registrations in server/main.py")
    print(f"2. Comment out or remove duplicate custom tools")
    print(f"3. Keep SDK tools as they provide complete official coverage")
    print(f"4. Test server startup to verify no more duplicates")
    
    return duplicates

if __name__ == "__main__":
    duplicates = find_duplicate_tools()
    print(f"\\n🏁 Found {len(duplicates)} total duplicates to resolve")