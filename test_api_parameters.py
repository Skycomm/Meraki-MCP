#!/usr/bin/env python3
"""
Simple test to verify our parameter improvements by checking the source code.
"""

import re
import os

def check_file_for_perpages(filepath, expected_patterns):
    """Check if a file contains the expected perPage patterns."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    results = []
    for pattern_name, pattern, expected in expected_patterns:
        matches = re.findall(pattern, content)
        if matches:
            # Check if any match has the expected value
            success = any(expected in match for match in matches)
            results.append((pattern_name, success, matches[0] if matches else None))
        else:
            results.append((pattern_name, False, None))
    
    return results

def main():
    print("="*60)
    print("PARAMETER IMPROVEMENT VERIFICATION")
    print("="*60)
    
    # Define what we're looking for
    checks = [
        {
            'file': 'server/tools_networks_additional.py',
            'patterns': [
                ('get_network_alerts_history perPage', r"kwargs\['perPage'\]\s*=\s*(\d+)", "1000"),
            ]
        },
        {
            'file': 'server/tools_appliance_additional.py',
            'patterns': [
                ('security_events perPage', r"kwargs\['perPage'\]\s*=\s*(\d+)", "1000"),
                ('security_events timespan', r"kwargs\['timespan'\]\s*=\s*(\d+)", "2678400"),
            ]
        },
        {
            'file': 'server/tools_networks.py',
            'patterns': [
                ('get_network_events perPage', r"kwargs\['perPage'\]\s*=\s*(\d+)", "1000"),
                ('get_network_clients perPage', r"kwargs\['perPage'\]\s*=\s*(\d+)", "1000"),
            ]
        },
        {
            'file': 'server/tools_wireless.py',
            'patterns': [
                ('wireless_clients perPage', r"kwargs\['perPage'\]\s*=\s*(\d+)", "1000"),
                ('lanIsolationEnabled display', r"lanIsolationEnabled", "lanIsolationEnabled"),
            ]
        },
        {
            'file': 'server/tools_organizations_additional.py',
            'patterns': [
                ('device_availabilities perPage', r"kwargs\['perPage'\]\s*=\s*(\d+)", "1000"),
            ]
        },
    ]
    
    all_results = []
    
    for check in checks:
        filepath = check['file']
        if os.path.exists(filepath):
            print(f"\n📁 Checking {filepath}:")
            print("-" * 40)
            results = check_file_for_perpages(filepath, check['patterns'])
            
            for pattern_name, success, match in results:
                if success:
                    print(f"  ✅ {pattern_name}: Found correct value")
                else:
                    print(f"  ❌ {pattern_name}: Not found or incorrect")
                all_results.append((f"{filepath}: {pattern_name}", success))
        else:
            print(f"\n❌ File not found: {filepath}")
            for pattern_name, _, _ in check['patterns']:
                all_results.append((f"{filepath}: {pattern_name}", False))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in all_results if success)
    total = len(all_results)
    
    print(f"\nResults: {passed}/{total} checks passed\n")
    
    for check_name, success in all_results:
        status = "✅" if success else "❌"
        print(f"{status} {check_name}")
    
    if passed == total:
        print("\n✅ ALL PARAMETER IMPROVEMENTS VERIFIED IN SOURCE CODE!")
    else:
        print("\n⚠️ Some improvements may be missing")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)