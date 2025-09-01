#!/usr/bin/env python3
"""
Comprehensive SDK Coverage Analysis
Compares our MCP server implementation against official Meraki SDK
"""

import meraki
import re
from pathlib import Path

def get_sdk_methods(category):
    """Get all SDK methods for a category"""
    dashboard = meraki.DashboardAPI('test', suppress_logging=True)
    if not hasattr(dashboard, category):
        return []
    obj = getattr(dashboard, category)
    return [m for m in dir(obj) if not m.startswith('_')]

def analyze_file_coverage(file_path, category):
    """Analyze which SDK methods are implemented in a file"""
    if not Path(file_path).exists():
        return set()
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find SDK method calls
    pattern = rf'meraki_client\.dashboard\.{category}\.(\w+)\('
    matches = re.findall(pattern, content)
    return set(matches)

def print_category_report(category, files):
    """Print detailed coverage report for a category"""
    sdk_methods = get_sdk_methods(category)
    if not sdk_methods:
        return 0, 0
    
    # Collect implementations from all files
    implemented = set()
    for file in files:
        implemented.update(analyze_file_coverage(file, category))
    
    total = len(sdk_methods)
    covered = len(implemented)
    percentage = (covered / total * 100) if total > 0 else 0
    
    print(f"\n{'='*80}")
    print(f"# {category.upper()} COVERAGE REPORT")
    print(f"{'='*80}")
    print(f"Total SDK Methods: {total}")
    print(f"Implemented: {covered} ({percentage:.1f}%)")
    print(f"Missing: {total - covered}")
    
    # Group methods by operation type
    create_methods = [m for m in sdk_methods if m.startswith('create')]
    update_methods = [m for m in sdk_methods if m.startswith('update')]
    delete_methods = [m for m in sdk_methods if m.startswith('delete') or m.startswith('remove')]
    get_methods = [m for m in sdk_methods if m.startswith('get')]
    other_methods = [m for m in sdk_methods if not any(m.startswith(p) for p in ['create', 'update', 'delete', 'remove', 'get'])]
    
    print(f"\nBy Operation Type:")
    print(f"  GET methods: {len([m for m in get_methods if m in implemented])}/{len(get_methods)}")
    print(f"  CREATE methods: {len([m for m in create_methods if m in implemented])}/{len(create_methods)}")
    print(f"  UPDATE methods: {len([m for m in update_methods if m in implemented])}/{len(update_methods)}")
    print(f"  DELETE methods: {len([m for m in delete_methods if m in implemented])}/{len(delete_methods)}")
    print(f"  OTHER methods: {len([m for m in other_methods if m in implemented])}/{len(other_methods)}")
    
    # Show missing critical methods
    missing = set(sdk_methods) - implemented
    if missing and percentage < 100:
        critical_missing = []
        
        # Prioritize commonly used operations
        for m in missing:
            if any(keyword in m.lower() for keyword in ['status', 'setting', 'config', 'policy', 'rule']):
                critical_missing.append(m)
        
        if critical_missing:
            print(f"\nCritical Missing Methods (top 10):")
            for method in sorted(critical_missing)[:10]:
                print(f"  - {method}")
    
    return covered, total

def main():
    """Run comprehensive coverage analysis"""
    base_path = "/Users/david/docker/cisco-meraki-mcp-server-tvi/server/"
    
    categories = {
        'switch': [
            base_path + 'tools_switch.py'
        ],
        'wireless': [
            base_path + 'tools_wireless.py',
            base_path + 'tools_wireless_advanced.py',
            base_path + 'tools_wireless_firewall.py',
            base_path + 'tools_wireless_ssid_features.py',
            base_path + 'tools_wireless_organization.py',
            base_path + 'tools_wireless_client_analytics.py',
            base_path + 'tools_wireless_infrastructure.py'
        ],
        'appliance': [
            base_path + 'tools_appliance.py',
            base_path + 'tools_appliance_additional.py',
            base_path + 'tools_appliance_firewall.py'
        ],
        'networks': [
            base_path + 'tools_networks.py',
            base_path + 'tools_networks_complete.py'
        ],
        'organizations': [
            base_path + 'tools_organizations_earlyAccess.py',
            base_path + 'tools_organizations_core.py',
            base_path + 'tools_organizations_adaptive_policy.py',
            base_path + 'tools_organizations_admin.py',
            base_path + 'tools_organizations_inventory.py',
            base_path + 'tools_organizations_licensing.py',
            base_path + 'tools_organizations_alerts.py',
            base_path + 'tools_organizations_misc.py',
            base_path + 'tools_organizations_config.py'
        ],
        'devices': [
            base_path + 'tools_devices.py'
        ],
        'camera': [
            base_path + 'tools_camera.py'
        ],
        'cellularGateway': [
            base_path + 'tools_cellularGateway.py'
        ],
        'sensor': [
            base_path + 'tools_sensor.py'
        ],
        'sm': [
            base_path + 'tools_sm.py'
        ],
        'insight': [
            base_path + 'tools_insight.py'
        ],
        'licensing': [
            base_path + 'tools_licensing.py'
        ]
    }
    
    print("🔍 CISCO MERAKI MCP SERVER - SDK COVERAGE ANALYSIS")
    print("="*80)
    
    total_covered = 0
    total_methods = 0
    category_stats = []
    
    # Analyze each category
    for category, files in categories.items():
        covered, total = print_category_report(category, files)
        if total > 0:
            total_covered += covered
            total_methods += total
            percentage = (covered / total * 100) if total > 0 else 0
            category_stats.append((category, covered, total, percentage))
    
    # Print summary
    print(f"\n{'='*80}")
    print("📊 OVERALL SUMMARY")
    print("="*80)
    
    # Sort by coverage percentage
    category_stats.sort(key=lambda x: x[3], reverse=True)
    
    print("\nCoverage by Category:")
    for cat, covered, total, pct in category_stats:
        bar_length = int(pct / 5)  # 20 char max bar
        bar = '█' * bar_length + '░' * (20 - bar_length)
        print(f"  {cat:20s} {bar} {covered:3d}/{total:3d} ({pct:5.1f}%)")
    
    overall_pct = (total_covered / total_methods * 100) if total_methods > 0 else 0
    print(f"\nTOTAL COVERAGE: {total_covered}/{total_methods} ({overall_pct:.1f}%)")
    
    # Highlight achievements and gaps
    print("\n✅ STRONG COVERAGE (>70%):")
    for cat, covered, total, pct in category_stats:
        if pct >= 70:
            print(f"  - {cat}: {pct:.1f}%")
    
    print("\n⚠️  NEEDS IMPROVEMENT (<50%):")
    for cat, covered, total, pct in category_stats:
        if pct < 50:
            print(f"  - {cat}: {pct:.1f}% (missing {total-covered} methods)")

if __name__ == "__main__":
    main()