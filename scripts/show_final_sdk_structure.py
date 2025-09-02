#!/usr/bin/env python3
"""
Show the final SDK structure with tool counts vs SDK coverage.
This shows what the structure will look like after reorganization.
"""

import json
from pathlib import Path

def load_coverage_data():
    """Load the SDK coverage report."""
    try:
        with open('sdk_coverage_report.json', 'r') as f:
            return json.load(f)
    except:
        return []

def count_tools_in_file(file_path):
    """Count @app.tool decorators in a file."""
    if not Path(file_path).exists():
        return 0
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Count @app.tool decorators
        import re
        matches = re.findall(r'@app\.tool\(', content)
        return len(matches)
    except:
        return 0

def analyze_current_state():
    """Analyze current modules and their tool counts.""" 
    
    # Current modules by category
    current_modules = {
        'administered': ['server/tools_administered.py'],
        'appliance': [
            'server/tools_appliance.py',
            'server/tools_appliance_additional.py', 
            'server/tools_appliance_firewall.py'
        ],
        'batch': ['server/tools_batch.py'],
        'camera': ['server/tools_camera.py'],
        'cellularGateway': ['server/tools_cellularGateway.py'],
        'devices': ['server/tools_devices.py'],
        'insight': ['server/tools_insight.py'],
        'licensing': ['server/tools_licensing.py'],
        'networks': [
            'server/tools_networks.py',
            'server/tools_networks_complete.py'
        ],
        'organizations': [
            'server/tools_organizations_core.py',
            'server/tools_organizations_admin.py',
            'server/tools_organizations_adaptive_policy.py',
            'server/tools_organizations_alerts.py',
            'server/tools_organizations_config.py',
            'server/tools_organizations_earlyAccess.py',
            'server/tools_organizations_inventory.py',
            'server/tools_organizations_licensing.py',
            'server/tools_organizations_misc.py'
        ],
        'sensor': ['server/tools_sensor.py'],
        'sm': ['server/tools_sm.py'],
        'switch': ['server/tools_switch.py'],
        'wireless': [
            'server/tools_wireless.py',
            'server/tools_wireless_advanced.py',
            'server/tools_wireless_client_analytics.py',
            'server/tools_wireless_firewall.py',
            'server/tools_wireless_infrastructure.py',
            'server/tools_wireless_organization.py',
            'server/tools_wireless_rf_profiles.py',
            'server/tools_wireless_ssid_features.py'
        ]
    }
    
    # Custom modules (non-SDK)
    custom_modules = [
        'server/tools_helpers.py',
        'server/tools_search.py', 
        'server/tools_analytics.py',
        'server/tools_alerts.py',
        'server/tools_live.py',
        'server/tools_monitoring.py',
        'server/tools_monitoring_dashboard.py',
        'server/tools_policy.py',
        'server/tools_vpn.py',
        'server/tools_beta.py',
        'server/tools_event_analysis.py',
        'server/tools_adaptive_policy.py',
        'server/tools_custom_helpers.py',
        'server/tools_custom_analytics.py',
        'server/tools_custom_alerts.py',
        'server/tools_custom_beta.py',
        'server/tools_custom_event_analysis.py',
        'server/tools_custom_live.py',
        'server/tools_custom_monitoring.py',
        'server/tools_custom_monitoring_dashboard.py',
        'server/tools_custom_policy.py',
        'server/tools_custom_search.py',
        'server/tools_custom_vpn.py'
    ]
    
    return current_modules, custom_modules

def show_final_structure():
    """Show the final SDK-aligned structure."""
    
    # SDK coverage data (from analysis)
    sdk_data = {
        'administered': {'sdk_methods': 4, 'implemented': 0, 'coverage': 0.0},
        'appliance': {'sdk_methods': 130, 'implemented': 57, 'coverage': 43.8},
        'batch': {'sdk_methods': 12, 'implemented': 12, 'coverage': 100.0},  # Estimated
        'camera': {'sdk_methods': 45, 'implemented': 8, 'coverage': 17.8},
        'cellularGateway': {'sdk_methods': 24, 'implemented': 24, 'coverage': 100.0},
        'devices': {'sdk_methods': 27, 'implemented': 12, 'coverage': 44.4},
        'insight': {'sdk_methods': 7, 'implemented': 7, 'coverage': 100.0},
        'licensing': {'sdk_methods': 8, 'implemented': 1, 'coverage': 12.5},
        'networks': {'sdk_methods': 114, 'implemented': 8, 'coverage': 7.0},
        'organizations': {'sdk_methods': 173, 'implemented': 109, 'coverage': 63.0},
        'sensor': {'sdk_methods': 18, 'implemented': 18, 'coverage': 100.0},
        'sm': {'sdk_methods': 49, 'implemented': 38, 'coverage': 77.6},
        'switch': {'sdk_methods': 101, 'implemented': 102, 'coverage': 101.0},  # 1 extra
        'wireless': {'sdk_methods': 116, 'implemented': 125, 'coverage': 107.8}  # 11 extra
    }
    
    current_modules, custom_modules = analyze_current_state()
    
    print("🎯 **FINAL SDK-ALIGNED STRUCTURE**")
    print("=" * 80)
    print()
    
    print("📦 **SDK MODULES** (14 files - exact 1:1 mapping with Meraki SDK):")
    print()
    
    total_sdk_methods = 0
    total_current_tools = 0
    total_missing = 0
    
    for category, data in sdk_data.items():
        sdk_methods = data['sdk_methods']
        current_tools = 0
        
        # Count current tools in this category
        if category in current_modules:
            for file_path in current_modules[category]:
                current_tools += count_tools_in_file(file_path)
        
        coverage = data['coverage']
        missing = max(0, sdk_methods - data['implemented'])
        
        total_sdk_methods += sdk_methods
        total_current_tools += current_tools
        total_missing += missing
        
        # Status indicators
        if coverage >= 100:
            status = "🟢 PERFECT"
        elif coverage >= 75:
            status = "🟡 GOOD"
        elif coverage >= 50:
            status = "🟠 PARTIAL"
        else:
            status = "🔴 MAJOR GAP"
        
        print(f"📂 **tools_SDK_{category}.py**")
        print(f"   Current Tools: {current_tools:3d} | SDK Target: {sdk_methods:3d} | Coverage: {coverage:5.1f}% {status}")
        
        if category == 'appliance':
            print(f"   ← Consolidate: tools_appliance*.py (3 files)")
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
            print(f"   📈 Need: +{missing} missing SDK methods")
        elif data['implemented'] > sdk_methods:
            extra = data['implemented'] - sdk_methods
            print(f"   📤 Move: {extra} extra methods → tools_CUSTOM_extensions.py")
        print()
    
    # Count custom tools
    custom_tool_count = 0
    print("🛠️  **CUSTOM MODULE** (1 file - all non-SDK functionality):")
    print()
    print("📂 **tools_CUSTOM_extensions.py**")
    
    for file_path in custom_modules:
        if Path(file_path).exists():
            tools_in_file = count_tools_in_file(file_path)
            custom_tool_count += tools_in_file
            print(f"   ← {file_path.replace('server/', '')}: {tools_in_file} tools")
    
    # Add extra methods from SDK modules
    extra_from_sdk = (data['implemented'] - sdk_data['switch']['sdk_methods']) + (sdk_data['wireless']['implemented'] - sdk_data['wireless']['sdk_methods'])
    extra_from_sdk = max(0, extra_from_sdk)
    
    print(f"   ← Plus {extra_from_sdk} extra methods from SDK modules")
    total_custom = custom_tool_count + extra_from_sdk
    print(f"   **Total Custom Tools**: ~{total_custom}")
    print()
    
    print("🎉 **SUMMARY:**")
    print(f"   • **15 total modules** (vs current 78)")
    print(f"   • **14 SDK modules**: {total_current_tools} current tools → {total_sdk_methods} SDK methods")
    print(f"   • **1 custom module**: ~{total_custom} extension tools")
    print(f"   • **Missing to implement**: {total_missing} SDK methods")
    print(f"   • **Coverage goal**: 100% (816/816 SDK methods)")
    print()
    
    print("📋 **IMPLEMENTATION PRIORITY:**")
    gaps = [(cat, data['sdk_methods'] - data['implemented']) for cat, data in sdk_data.items() 
           if data['implemented'] < data['sdk_methods']]
    gaps.sort(key=lambda x: x[1], reverse=True)
    
    for i, (category, missing) in enumerate(gaps[:5]):
        priority = "🔥 HIGH" if i < 2 else "🔶 MEDIUM" if i < 4 else "🟢 LOW"
        print(f"   {priority}: {category} (+{missing} methods)")

def main():
    """Show the final structure analysis."""
    show_final_structure()

if __name__ == '__main__':
    main()