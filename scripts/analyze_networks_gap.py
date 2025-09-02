#!/usr/bin/env python3
"""
Analyze Networks SDK gap - what methods are we missing?
"""

import meraki
import re
from pathlib import Path

def get_sdk_methods():
    """Get all Networks SDK methods."""
    dashboard = meraki.DashboardAPI('dummy', suppress_logging=True)
    methods = [m for m in dir(dashboard.networks) if not m.startswith('_') and callable(getattr(dashboard.networks, m))]
    return sorted(methods)

def get_implemented_methods():
    """Get methods we've currently implemented."""
    implemented = set()
    
    network_files = [
        'server/tools_networks.py',
        'server/tools_networks_complete.py'
    ]
    
    for file_path in network_files:
        if not Path(file_path).exists():
            continue
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Find SDK method calls - look for meraki_client.dashboard.networks.METHOD_NAME(
            pattern = r'meraki_client\.dashboard\.networks\.(\w+)\s*\('
            matches = re.findall(pattern, content)
            implemented.update(matches)
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    return implemented

def analyze_gap():
    """Analyze what methods are missing."""
    sdk_methods = set(get_sdk_methods())
    implemented_methods = get_implemented_methods()
    
    print("📊 NETWORKS SDK GAP ANALYSIS")
    print("=" * 60)
    print(f"SDK Methods: {len(sdk_methods)}")
    print(f"Implemented: {len(implemented_methods)}")
    print(f"Coverage: {len(implemented_methods)/len(sdk_methods)*100:.1f}%")
    print()
    
    missing = sdk_methods - implemented_methods
    extra = implemented_methods - sdk_methods
    
    print(f"❌ MISSING METHODS ({len(missing)}):")
    missing_by_category = {}
    
    for method in sorted(missing):
        category = 'Other'
        if 'FloorPlan' in method:
            category = 'Floor Plans'
        elif 'GroupPolicy' in method or 'GroupPolicies' in method:
            category = 'Group Policies'
        elif 'Firmware' in method:
            category = 'Firmware'
        elif 'Client' in method:
            category = 'Client Management'
        elif 'Webhook' in method:
            category = 'Webhooks'
        elif 'Alert' in method:
            category = 'Alerts'
        elif 'Traffic' in method or 'Netflow' in method:
            category = 'Traffic Analysis'
        elif 'Vlan' in method:
            category = 'VLANs'
        elif 'Device' in method or method in ['bindNetwork', 'unbindNetwork', 'claimNetworkDevices', 'removeNetworkDevices']:
            category = 'Device Management'
        elif 'Pii' in method:
            category = 'PII Requests'
        elif 'Mqtt' in method:
            category = 'MQTT'
        elif 'Auth' in method or 'Splash' in method:
            category = 'Authentication'
        
        if category not in missing_by_category:
            missing_by_category[category] = []
        missing_by_category[category].append(method)
    
    for category, methods in missing_by_category.items():
        print(f"\n🔸 {category} ({len(methods)} methods):")
        for method in methods[:5]:  # Show first 5
            print(f"   - {method}")
        if len(methods) > 5:
            print(f"   ... and {len(methods)-5} more")
    
    if extra:
        print(f"\n⚠️  EXTRA METHODS ({len(extra)}) - Not in SDK:")
        for method in sorted(extra):
            print(f"   - {method}")
    
    print(f"\n📈 PRIORITY IMPLEMENTATION ORDER:")
    priority_categories = [
        ('Floor Plans', 'Device placement and location'),
        ('Group Policies', 'Network access control'), 
        ('Firmware', 'Update management'),
        ('Device Management', 'Claiming and binding'),
        ('VLANs', 'Network segmentation'),
        ('Traffic Analysis', 'Monitoring and shaping'),
        ('Webhooks', 'Event notifications'),
        ('Client Management', 'User management')
    ]
    
    for i, (category, description) in enumerate(priority_categories, 1):
        if category in missing_by_category:
            count = len(missing_by_category[category])
            print(f"   {i}. {category}: {count} methods - {description}")

if __name__ == '__main__':
    analyze_gap()