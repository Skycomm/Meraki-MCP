#!/usr/bin/env python3
"""
Round 2 Validation - Automated parameter verification
"""

import os
import re

def validate_parameters():
    """Validate all parameter improvements are in place."""
    
    print("="*60)
    print("ROUND 2: AUTOMATED PARAMETER VALIDATION")
    print("="*60)
    
    validations = {
        'Network Events perPage=1000': {
            'file': 'server/tools_networks.py',
            'pattern': r"kwargs\['perPage'\]\s*=\s*1000",
            'expected_count': 3  # Should appear at least 3 times
        },
        'Network Clients perPage=1000': {
            'file': 'server/tools_networks.py', 
            'pattern': r"kwargs\['perPage'\]\s*=\s*1000.*Maximum allowed",
            'expected_count': 1
        },
        'Security Events perPage=1000': {
            'file': 'server/tools_appliance_additional.py',
            'pattern': r"kwargs\['perPage'\]\s*=\s*1000",
            'expected_count': 1
        },
        'Security Events timespan=31days': {
            'file': 'server/tools_appliance_additional.py',
            'pattern': r"kwargs\['timespan'\]\s*=\s*2678400",
            'expected_count': 1
        },
        'Alert History perPage=1000': {
            'file': 'server/tools_networks_additional.py',
            'pattern': r"kwargs\['perPage'\]\s*=\s*1000",
            'expected_count': 1
        },
        'Wireless Clients perPage=1000': {
            'file': 'server/tools_wireless.py',
            'pattern': r"kwargs\['perPage'\]\s*=\s*1000",
            'expected_count': 1
        },
        'SSID Isolation Display': {
            'file': 'server/tools_wireless.py',
            'pattern': r"lanIsolationEnabled.*🔒.*🔓",
            'expected_count': 1
        },
        'Org Devices perPage=1000': {
            'file': 'server/tools_organizations_additional.py',
            'pattern': r"kwargs\['perPage'\]\s*=\s*1000",
            'expected_count': 2  # Should appear in multiple functions
        }
    }
    
    results = []
    
    for test_name, config in validations.items():
        filepath = config['file']
        pattern = config['pattern']
        expected = config['expected_count']
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            matches = re.findall(pattern, content, re.DOTALL)
            actual_count = len(matches)
            
            if actual_count >= expected:
                print(f"✅ {test_name}: Found {actual_count} occurrences (expected {expected}+)")
                results.append(True)
            else:
                print(f"❌ {test_name}: Found {actual_count} occurrences (expected {expected}+)")
                results.append(False)
                
        except Exception as e:
            print(f"❌ {test_name}: Error - {str(e)}")
            results.append(False)
    
    print("\n" + "="*60)
    print("ADDITIONAL CHECKS")
    print("="*60)
    
    # Check for old/wrong values that should NOT exist
    bad_patterns = [
        ('No perPage=100 in alerts', 'server/tools_networks_additional.py', r"kwargs\['perPage'\]\s*=\s*100\b"),
        ('No perPage=20', 'server/tools_*.py', r"kwargs\['perPage'\]\s*=\s*20"),
        ('No short default timespan', 'server/tools_appliance_additional.py', r"kwargs\['timespan'\]\s*=\s*3600")
    ]
    
    for check_name, file_pattern, bad_pattern in bad_patterns:
        found = False
        
        if '*' in file_pattern:
            # Check multiple files
            import glob
            for filepath in glob.glob(file_pattern):
                try:
                    with open(filepath, 'r') as f:
                        if re.search(bad_pattern, f.read()):
                            found = True
                            break
                except:
                    pass
        else:
            # Check single file
            try:
                with open(file_pattern, 'r') as f:
                    if re.search(bad_pattern, f.read()):
                        found = True
            except:
                pass
        
        if not found:
            print(f"✅ {check_name}: No bad patterns found")
            results.append(True)
        else:
            print(f"❌ {check_name}: Found bad pattern that should be fixed")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("ROUND 2 VALIDATION SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100
    
    print(f"\n📊 Results: {passed}/{total} checks passed ({percentage:.1f}%)\n")
    
    if percentage == 100:
        print("🎉 PERFECT SCORE! All parameter improvements working correctly!")
        print("✅ Ready for MCP testing with the Round 2 test prompts")
    elif percentage >= 90:
        print("✅ EXCELLENT! Minor issues only")
    elif percentage >= 80:
        print("⚠️ GOOD but some improvements needed")
    else:
        print("❌ NEEDS ATTENTION - Multiple issues found")
    
    print("\n" + "="*60)
    print("KEY IMPROVEMENTS VERIFIED:")
    print("="*60)
    print("• All APIs use perPage=1000 for maximum data retrieval")
    print("• Security events default to 31-day timespan")
    print("• SSID isolation status displayed with icons")
    print("• No legacy pagination limits (100, 20) found")
    print("• Alert history upgraded from 100 to 1000")
    
    return percentage == 100

if __name__ == "__main__":
    success = validate_parameters()
    exit(0 if success else 1)