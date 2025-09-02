#!/usr/bin/env python3
"""
Reorganize modules to have clean SDK alignment:
- tools_SDK_<category>.py for official SDK categories (14 modules)
- tools_CUSTOM_<feature>.py for non-SDK functionality (1 module)

This creates perfect 1:1 mapping with official Meraki SDK.
"""

import os
import shutil
from pathlib import Path

# Official SDK categories (from meraki.DashboardAPI)
SDK_CATEGORIES = [
    'administered',
    'appliance', 
    'batch',
    'camera',
    'cellularGateway',
    'devices',
    'insight',
    'licensing',
    'networks',
    'organizations',
    'sensor',
    'sm',
    'switch',
    'wireless'
]

def create_sdk_module_plan():
    """Create mapping from current modules to SDK modules."""
    
    # Current modules that should become SDK modules
    current_modules = {
        # Direct matches (already correct)
        'tools_administered.py': 'tools_SDK_administered.py',
        'tools_batch.py': 'tools_SDK_batch.py', 
        'tools_camera.py': 'tools_SDK_camera.py',
        'tools_cellularGateway.py': 'tools_SDK_cellularGateway.py',
        'tools_devices.py': 'tools_SDK_devices.py',
        'tools_insight.py': 'tools_SDK_insight.py',
        'tools_licensing.py': 'tools_SDK_licensing.py',
        'tools_networks.py': 'tools_SDK_networks.py',
        'tools_sensor.py': 'tools_SDK_sensor.py',
        'tools_sm.py': 'tools_SDK_sm.py',
        'tools_switch.py': 'tools_SDK_switch.py',
        
        # Consolidate split categories
        'tools_appliance.py': 'tools_SDK_appliance.py',  # Main appliance file
        # tools_appliance_additional.py + tools_appliance_firewall.py → merge into SDK_appliance
        
        # Consolidate all wireless modules
        'tools_wireless.py': 'tools_SDK_wireless.py',  # Main wireless file
        # All tools_wireless_*.py → merge into SDK_wireless
        
        # Consolidate all organizations modules  
        'tools_organizations_core.py': 'tools_SDK_organizations.py',  # Main orgs file
        # All tools_organizations_*.py → merge into SDK_organizations
        
        # Networks extensions
        'tools_networks_complete.py': 'MERGE_INTO_SDK_networks'  # Extended network tools
    }
    
    # Modules that should become CUSTOM (non-SDK)
    custom_modules = [
        'tools_helpers.py',
        'tools_search.py',
        'tools_analytics.py', 
        'tools_alerts.py',
        'tools_live.py',
        'tools_monitoring.py',
        'tools_monitoring_dashboard.py',
        'tools_policy.py',
        'tools_vpn.py',
        'tools_beta.py',
        'tools_event_analysis.py',
        'tools_adaptive_policy.py'  # Network-level adaptive policy
    ]
    
    return current_modules, custom_modules

def print_reorganization_plan():
    """Show what the reorganization will look like."""
    current_modules, custom_modules = create_sdk_module_plan()
    
    print("🎯 SDK MODULE REORGANIZATION PLAN")
    print("=" * 60)
    print()
    
    print("✅ OFFICIAL SDK CATEGORIES (14 modules):")
    print("These will match the official Meraki SDK exactly:")
    print()
    
    for category in SDK_CATEGORIES:
        print(f"📦 tools_SDK_{category}.py")
        
        if category == 'appliance':
            print(f"   ← Consolidate: tools_appliance.py + tools_appliance_additional.py + tools_appliance_firewall.py")
        elif category == 'wireless':
            print(f"   ← Consolidate: All 8 tools_wireless*.py files (180 tools)")
        elif category == 'organizations':
            print(f"   ← Consolidate: All 9 tools_organizations*.py files (115 tools)")
        elif category == 'networks':
            print(f"   ← Merge: tools_networks.py + tools_networks_complete.py")
        else:
            print(f"   ← Rename: tools_{category}.py")
        print()
    
    print("🛠️  CUSTOM FUNCTIONALITY (1 module):")
    print("All non-SDK tools consolidated:")
    print()
    print("📦 tools_CUSTOM_extensions.py")
    print("   ← Consolidate all custom/helper modules:")
    for module in custom_modules:
        print(f"     - {module}")
    print()
    
    print("🎉 RESULT:")
    print("- 14 SDK modules (perfect 1:1 mapping)")
    print("- 1 custom module (all extensions)")  
    print("- 15 total modules (vs current 42)")
    print("- Easy SDK comparison and gap analysis")
    print("- Clean separation of SDK vs custom functionality")

def main():
    """Show the reorganization plan."""
    print_reorganization_plan()
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Review this plan")
    print("2. Run consolidation script")
    print("3. Update profiles.py")
    print("4. Update main.py imports")
    print("5. Test all profiles")

if __name__ == '__main__':
    main()