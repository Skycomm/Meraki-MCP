#!/usr/bin/env python3
"""
Comprehensive SDK Coverage Analysis
Compare our MCP server tools against the official Meraki SDK to identify gaps.
"""

import meraki
import re
from pathlib import Path
import json

def get_sdk_methods(category):
    """Get all methods for an SDK category."""
    try:
        dashboard = meraki.DashboardAPI('dummy_key', suppress_logging=True)
        if not hasattr(dashboard, category):
            return []
        obj = getattr(dashboard, category)
        methods = [m for m in dir(obj) if not m.startswith('_') and callable(getattr(obj, m))]
        return sorted(methods)
    except Exception as e:
        print(f"Error getting SDK methods for {category}: {e}")
        return []

def analyze_file_coverage(file_paths, category):
    """Analyze which SDK methods are implemented in our files."""
    implemented = set()
    
    for file_path in file_paths:
        if not Path(file_path).exists():
            continue
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Find SDK method calls in the format: meraki_client.dashboard.category.method(
            pattern = rf'meraki_client\.dashboard\.{category}\.(\w+)\s*\('
            matches = re.findall(pattern, content)
            implemented.update(matches)
            
            # Also check for direct dashboard calls
            pattern_alt = rf'dashboard\.{category}\.(\w+)\s*\('
            matches_alt = re.findall(pattern_alt, content)
            implemented.update(matches_alt)
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    return implemented

def get_our_tool_files():
    """Get mapping of SDK categories to our tool files."""
    base_path = Path('server')
    
    category_files = {
        'administered': [base_path / 'tools_administered.py'],
        'appliance': [
            base_path / 'tools_appliance.py',
            base_path / 'tools_appliance_additional.py', 
            base_path / 'tools_appliance_firewall.py'
        ],
        'batch': [base_path / 'tools_batch.py'],
        'camera': [base_path / 'tools_camera.py'],
        'cellularGateway': [base_path / 'tools_cellularGateway.py'],
        'devices': [base_path / 'tools_devices.py'],
        'insight': [base_path / 'tools_insight.py'],
        'licensing': [base_path / 'tools_licensing.py'],
        'networks': [
            base_path / 'tools_networks.py',
            base_path / 'tools_networks_complete.py'
        ],
        'organizations': [
            base_path / 'tools_organizations_core.py',
            base_path / 'tools_organizations_admin.py',
            base_path / 'tools_organizations_adaptive_policy.py',
            base_path / 'tools_organizations_alerts.py',
            base_path / 'tools_organizations_config.py',
            base_path / 'tools_organizations_earlyAccess.py',
            base_path / 'tools_organizations_inventory.py',
            base_path / 'tools_organizations_licensing.py',
            base_path / 'tools_organizations_misc.py'
        ],
        'sensor': [base_path / 'tools_sensor.py'],
        'sm': [base_path / 'tools_sm.py'],
        'switch': [base_path / 'tools_switch.py'],
        'wireless': [
            base_path / 'tools_wireless.py',
            base_path / 'tools_wireless_advanced.py',
            base_path / 'tools_wireless_client_analytics.py',
            base_path / 'tools_wireless_firewall.py',
            base_path / 'tools_wireless_infrastructure.py',
            base_path / 'tools_wireless_organization.py',
            base_path / 'tools_wireless_rf_profiles.py',
            base_path / 'tools_wireless_ssid_features.py'
        ]
    }
    
    return category_files

def analyze_category_coverage(category, file_paths):
    """Analyze coverage for a single SDK category."""
    print(f"\n{'='*80}")
    print(f"📊 ANALYZING: {category.upper()}")
    print('='*80)
    
    # Get SDK methods
    sdk_methods = get_sdk_methods(category)
    if not sdk_methods:
        print(f"❌ Could not get SDK methods for {category}")
        return None
    
    # Get our implemented methods
    implemented = analyze_file_coverage(file_paths, category)
    
    # Calculate coverage
    total_sdk = len(sdk_methods)
    total_implemented = len(implemented)
    coverage_pct = (total_implemented / total_sdk * 100) if total_sdk > 0 else 0
    
    print(f"📈 SDK Methods: {total_sdk}")
    print(f"✅ Implemented: {total_implemented}")
    print(f"📊 Coverage: {coverage_pct:.1f}%")
    
    # Missing methods
    missing = set(sdk_methods) - implemented
    if missing:
        print(f"\n❌ MISSING METHODS ({len(missing)}):")
        for method in sorted(missing)[:10]:  # Show first 10
            print(f"   - {method}")
        if len(missing) > 10:
            print(f"   ... and {len(missing)-10} more")
    
    # Extra methods (not in SDK - might be custom or deprecated)
    extra = implemented - set(sdk_methods)
    if extra:
        print(f"\n⚠️  EXTRA METHODS ({len(extra)}) - Not in current SDK:")
        for method in sorted(extra)[:5]:  # Show first 5
            print(f"   - {method}")
        if len(extra) > 5:
            print(f"   ... and {len(extra)-5} more")
    
    # Method type analysis
    if sdk_methods:
        get_methods = [m for m in sdk_methods if m.startswith('get')]
        create_methods = [m for m in sdk_methods if m.startswith('create')]
        update_methods = [m for m in sdk_methods if m.startswith('update')]
        delete_methods = [m for m in sdk_methods if m.startswith('delete')]
        
        get_impl = len([m for m in get_methods if m in implemented])
        create_impl = len([m for m in create_methods if m in implemented])
        update_impl = len([m for m in update_methods if m in implemented])
        delete_impl = len([m for m in delete_methods if m in implemented])
        
        print(f"\n📋 BY OPERATION TYPE:")
        print(f"   GET:    {get_impl}/{len(get_methods)} ({get_impl/len(get_methods)*100:.1f}%)" if get_methods else "   GET: 0/0")
        print(f"   CREATE: {create_impl}/{len(create_methods)} ({create_impl/len(create_methods)*100:.1f}%)" if create_methods else "   CREATE: 0/0")
        print(f"   UPDATE: {update_impl}/{len(update_methods)} ({update_impl/len(update_methods)*100:.1f}%)" if update_methods else "   UPDATE: 0/0")
        print(f"   DELETE: {delete_impl}/{len(delete_methods)} ({delete_impl/len(delete_methods)*100:.1f}%)" if delete_methods else "   DELETE: 0/0")
    
    return {
        'category': category,
        'sdk_methods': total_sdk,
        'implemented': total_implemented, 
        'coverage_pct': coverage_pct,
        'missing': list(missing),
        'extra': list(extra),
        'files': [str(f) for f in file_paths if f.exists()]
    }

def main():
    """Run comprehensive SDK coverage analysis."""
    print("🔍 COMPREHENSIVE SDK COVERAGE ANALYSIS")
    print("Comparing our MCP implementation vs Official Meraki SDK")
    print("="*80)
    
    category_files = get_our_tool_files()
    results = []
    
    # Analyze each category
    for category, file_paths in category_files.items():
        result = analyze_category_coverage(category, file_paths)
        if result:
            results.append(result)
    
    # Overall summary
    print(f"\n{'='*80}")
    print("🎯 OVERALL COVERAGE SUMMARY")
    print("="*80)
    
    total_sdk_methods = sum(r['sdk_methods'] for r in results)
    total_implemented = sum(r['implemented'] for r in results)
    overall_coverage = (total_implemented / total_sdk_methods * 100) if total_sdk_methods > 0 else 0
    
    print(f"📊 Total SDK Methods: {total_sdk_methods}")
    print(f"✅ Total Implemented: {total_implemented}")
    print(f"📈 Overall Coverage: {overall_coverage:.1f}%")
    
    # Coverage by category (sorted by coverage)
    print(f"\n📋 COVERAGE BY CATEGORY:")
    results_sorted = sorted(results, key=lambda x: x['coverage_pct'], reverse=True)
    
    for result in results_sorted:
        bar_length = int(result['coverage_pct'] / 5)  # 20 chars max
        bar = '█' * bar_length + '░' * (20 - bar_length)
        print(f"  {result['category']:15s} {bar} {result['implemented']:3d}/{result['sdk_methods']:3d} ({result['coverage_pct']:5.1f}%)")
    
    # Categories needing attention
    print(f"\n🎯 PRIORITIES FOR EXPANSION:")
    low_coverage = [r for r in results if r['coverage_pct'] < 80]
    for result in sorted(low_coverage, key=lambda x: x['sdk_methods'], reverse=True):
        missing_count = len(result['missing'])
        print(f"  📦 {result['category']:15s} - Missing {missing_count:3d} methods ({result['coverage_pct']:5.1f}% coverage)")
    
    # Save detailed results
    output_file = 'sdk_coverage_report.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Detailed report saved to: {output_file}")

if __name__ == '__main__':
    main()