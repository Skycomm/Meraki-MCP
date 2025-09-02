#!/usr/bin/env python3
"""
Consolidate existing modules into SDK-aligned structure:
- tools_SDK_<category>.py for official SDK methods only
- tools_CUSTOM_extensions.py for all non-SDK methods
"""

import os
import shutil
from pathlib import Path
import re

# Official SDK categories from coverage analysis
SDK_CATEGORIES = {
    'administered': {'methods': 4, 'current_tools': 0},
    'appliance': {'methods': 130, 'current_tools': 57},
    'batch': {'methods': 12, 'current_tools': 12},  # Estimated from existing
    'camera': {'methods': 45, 'current_tools': 8},
    'cellularGateway': {'methods': 24, 'current_tools': 24},
    'devices': {'methods': 27, 'current_tools': 12},
    'insight': {'methods': 7, 'current_tools': 7},
    'licensing': {'methods': 8, 'current_tools': 1},
    'networks': {'methods': 114, 'current_tools': 8},
    'organizations': {'methods': 173, 'current_tools': 109},
    'sensor': {'methods': 18, 'current_tools': 18},
    'sm': {'methods': 49, 'current_tools': 38},
    'switch': {'methods': 101, 'current_tools': 102},  # 1 extra method
    'wireless': {'methods': 116, 'current_tools': 125}  # 11 extra methods
}

# Current module mapping to SDK categories
CURRENT_TO_SDK_MAPPING = {
    # Direct SDK matches (rename only)
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
    'tools_appliance.py': 'tools_SDK_appliance.py',
    'tools_appliance_additional.py': 'MERGE_INTO_SDK_appliance',
    'tools_appliance_firewall.py': 'MERGE_INTO_SDK_appliance',
    'tools_appliance_consolidated.py': 'MERGE_INTO_SDK_appliance',
    
    # Consolidate all organizations modules
    'tools_organizations_core.py': 'tools_SDK_organizations.py',
    'tools_organizations_admin.py': 'MERGE_INTO_SDK_organizations', 
    'tools_organizations_adaptive_policy.py': 'MERGE_INTO_SDK_organizations',
    'tools_organizations_alerts.py': 'MERGE_INTO_SDK_organizations',
    'tools_organizations_config.py': 'MERGE_INTO_SDK_organizations',
    'tools_organizations_earlyAccess.py': 'MERGE_INTO_SDK_organizations',
    'tools_organizations_inventory.py': 'MERGE_INTO_SDK_organizations',
    'tools_organizations_licensing.py': 'MERGE_INTO_SDK_organizations',
    'tools_organizations_misc.py': 'MERGE_INTO_SDK_organizations',
    
    # Consolidate all wireless modules  
    'tools_wireless.py': 'tools_SDK_wireless.py',
    'tools_wireless_advanced.py': 'MERGE_INTO_SDK_wireless',
    'tools_wireless_client_analytics.py': 'MERGE_INTO_SDK_wireless',
    'tools_wireless_firewall.py': 'MERGE_INTO_SDK_wireless', 
    'tools_wireless_infrastructure.py': 'MERGE_INTO_SDK_wireless',
    'tools_wireless_organization.py': 'MERGE_INTO_SDK_wireless',
    'tools_wireless_rf_profiles.py': 'MERGE_INTO_SDK_wireless',
    'tools_wireless_ssid_features.py': 'MERGE_INTO_SDK_wireless',
    
    # Extended networks (merge with base networks)
    'tools_networks_complete.py': 'MERGE_INTO_SDK_networks',
}

# All custom/helper modules → tools_CUSTOM_extensions.py
CUSTOM_MODULES = [
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
    'tools_adaptive_policy.py',  # Network-level adaptive policy
    'tools_custom_helpers.py',
    'tools_custom_analytics.py',
    'tools_custom_alerts.py',
    'tools_custom_beta.py',
    'tools_custom_event_analysis.py',
    'tools_custom_live.py',
    'tools_custom_monitoring.py',
    'tools_custom_monitoring_dashboard.py',
    'tools_custom_policy.py',
    'tools_custom_search.py',
    'tools_custom_vpn.py'
]

def print_reorganization_plan():
    """Print the complete reorganization plan."""
    print("🎯 COMPLETE SDK MODULE REORGANIZATION")
    print("=" * 80)
    print()
    
    print("📦 **TARGET: 15 MODULES TOTAL**")
    print("   • 14 SDK modules (tools_SDK_*.py)")
    print("   • 1 custom module (tools_CUSTOM_extensions.py)")
    print()
    
    print("🔄 **FROM CURRENT STATE:**")
    print(f"   • Current: 78 modules, 833 tools")
    print(f"   • SDK Coverage: 62.4% (509/816 methods)")
    print()
    
    print("✅ **SDK MODULES** (14 files, exact 1:1 SDK mapping):")
    print()
    
    for category, data in SDK_CATEGORIES.items():
        current_tools = data['current_tools']
        sdk_methods = data['methods']
        coverage = (current_tools / sdk_methods * 100) if sdk_methods > 0 else 0
        missing = max(0, sdk_methods - current_tools)
        
        status = "🟢 PERFECT" if coverage >= 100 else "🟡 PARTIAL" if coverage >= 50 else "🔴 MAJOR GAP"
        
        print(f"📂 tools_SDK_{category}.py")
        print(f"   Current: {current_tools:3d} tools | SDK Target: {sdk_methods:3d} methods | {coverage:5.1f}% coverage {status}")
        
        if category == 'appliance':
            print(f"   ← Consolidate: tools_appliance*.py (4 files)")
        elif category == 'organizations': 
            print(f"   ← Consolidate: tools_organizations*.py (9 files)")
        elif category == 'wireless':
            print(f"   ← Consolidate: tools_wireless*.py (8 files)")
        elif category == 'networks':
            print(f"   ← Merge: tools_networks*.py (2 files)")
        elif current_tools > 0:
            print(f"   ← Rename: tools_{category}.py")
        else:
            print(f"   ← Create new (implement {sdk_methods} methods)")
            
        if missing > 0:
            print(f"   📈 NEED: +{missing} missing SDK methods")
        print()
    
    print("🛠️  **CUSTOM MODULE** (1 file, all non-SDK functionality):")
    print()
    print("📂 tools_CUSTOM_extensions.py")
    print("   ← Consolidate all custom/helper modules:")
    print(f"   • {len(CUSTOM_MODULES)} current custom modules")
    print("   • 21 extra methods from SDK modules (non-SDK methods)")
    print("   • All helpers, analytics, monitoring, VPN, etc.")
    print()
    
    print("🎉 **FINAL RESULT:**")
    print("   • 15 total modules (vs current 78)")
    print("   • 14 SDK modules with 100% coverage (816 methods)")
    print("   • 1 custom module with all extensions (~70 tools)")
    print("   • Perfect SDK alignment for easy comparison")
    print("   • Clean separation of SDK vs custom functionality")
    print()
    
    print("📋 **IMPLEMENTATION PRIORITIES:**")
    print("   🔥 Phase 1: Networks (+106 methods), Appliance (+74 methods)")
    print("   🔶 Phase 2: Organizations (+66 methods), Camera (+39 methods)")
    print("   🟢 Phase 3: Complete remaining categories (+22 methods)")

def main():
    """Show the reorganization plan without executing it."""
    print_reorganization_plan()
    
    print("\n" + "=" * 60)
    print("⚠️  THIS IS A PLAN ONLY - NO CHANGES MADE")
    print("To execute:")
    print("1. Review this structure")
    print("2. Confirm the approach")
    print("3. Run actual consolidation script")

if __name__ == '__main__':
    main()