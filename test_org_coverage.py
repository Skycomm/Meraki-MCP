#!/usr/bin/env python3
"""
Comprehensive Organizations Coverage Test
Tests all SDK methods and compares with implementation
"""

import meraki
from server.main import app, meraki as meraki_client

# System test values  
TEST_ORG_ID = "686470"  # Skycomm
TEST_NETWORK_ID = "L_726205439913500692"  # Reserve St
TEST_DEVICE_SERIAL = "Q2PD-JL52-H3B2"  # Office AP

def test_organizations_coverage():
    """Test Organizations SDK coverage"""
    dashboard = meraki.DashboardAPI('test', suppress_logging=True)
    sdk_methods = [m for m in dir(dashboard.organizations) if not m.startswith('_')]
    
    print("🏢 ORGANIZATIONS SDK COVERAGE ANALYSIS")
    print("=" * 80)
    print(f"Total SDK Methods: {len(sdk_methods)}")
    
    # Test each method category
    results = {
        'GET': {'success': 0, 'failed': 0, 'methods': []},
        'CREATE': {'success': 0, 'failed': 0, 'methods': []},
        'UPDATE': {'success': 0, 'failed': 0, 'methods': []},
        'DELETE': {'success': 0, 'failed': 0, 'methods': []},
        'OTHER': {'success': 0, 'failed': 0, 'methods': []}
    }
    
    for method in sdk_methods:
        # Categorize method
        if method.startswith('get'):
            category = 'GET'
        elif method.startswith('create'):
            category = 'CREATE'
        elif method.startswith('update'):
            category = 'UPDATE'
        elif method.startswith('delete') or method.startswith('remove'):
            category = 'DELETE'
        else:
            category = 'OTHER'
        
        # Try to call method (read-only test)
        if category == 'GET':
            try:
                sdk_func = getattr(meraki_client.dashboard.organizations, method)
                
                # Determine required parameters
                if 'Organization' in method and 'Organizations' not in method:
                    # Single org methods need org_id
                    if 'Inventory' in method and 'Onboarding' in method:
                        # Onboarding needs deviceType
                        result = sdk_func(TEST_ORG_ID, deviceType='switch', perPage=5)
                    elif any(x in method for x in ['PerDevice', 'ByDevice', 'BySwitch']):
                        # Per-device methods need special pagination
                        result = sdk_func(TEST_ORG_ID, perPage=20)
                    else:
                        result = sdk_func(TEST_ORG_ID, perPage=50)
                else:
                    # List all orgs
                    result = sdk_func()
                
                results[category]['success'] += 1
                results[category]['methods'].append(f"✅ {method}")
            except Exception as e:
                results[category]['failed'] += 1
                error_msg = str(e)
                if 'missing' in error_msg.lower():
                    results[category]['methods'].append(f"❌ {method} - Missing parameters")
                elif '404' in error_msg:
                    results[category]['methods'].append(f"⚠️  {method} - Not found (may need setup)")
                else:
                    results[category]['methods'].append(f"❌ {method} - {error_msg[:50]}")
        else:
            # Non-GET methods - just check if implemented
            try:
                sdk_func = getattr(meraki_client.dashboard.organizations, method)
                results[category]['success'] += 1
                results[category]['methods'].append(f"✓ {method} (not tested)")
            except AttributeError:
                results[category]['failed'] += 1
                results[category]['methods'].append(f"✗ {method} (not implemented)")
    
    # Print results
    print("\n📊 RESULTS BY OPERATION TYPE:")
    print("-" * 80)
    
    for category in ['GET', 'CREATE', 'UPDATE', 'DELETE', 'OTHER']:
        data = results[category]
        total = data['success'] + data['failed']
        if total > 0:
            percentage = (data['success'] / total * 100) if total > 0 else 0
            print(f"\n{category} Methods: {data['success']}/{total} ({percentage:.1f}%)")
            
            # Show first 10 methods
            for method in data['methods'][:10]:
                print(f"  {method}")
            if len(data['methods']) > 10:
                print(f"  ... and {len(data['methods']) - 10} more")
    
    # Summary
    total_success = sum(r['success'] for r in results.values())
    total_methods = len(sdk_methods)
    coverage = (total_success / total_methods * 100) if total_methods > 0 else 0
    
    print("\n" + "=" * 80)
    print(f"📈 OVERALL COVERAGE: {total_success}/{total_methods} ({coverage:.1f}%)")
    
    if coverage < 100:
        print("\n⚠️  MISSING CRITICAL METHODS:")
        missing = []
        for category in results.values():
            for method in category['methods']:
                if '❌' in method or '✗' in method:
                    missing.append(method)
        
        for method in missing[:15]:
            print(f"  {method}")
        if len(missing) > 15:
            print(f"  ... and {len(missing) - 15} more")

if __name__ == "__main__":
    test_organizations_coverage()