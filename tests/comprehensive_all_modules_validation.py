#!/usr/bin/env python3
"""
Comprehensive 1:1 validation test for ALL 13 SDK modules.
Validates perfect mapping with official Cisco Meraki SDK.
"""

import meraki
import subprocess
import sys
from datetime import datetime

def validate_all_modules():
    """Comprehensive validation of all 13 SDK modules."""
    
    print("🔍 COMPREHENSIVE ALL MODULES 1:1 SDK VALIDATION")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Define all SDK modules with expected counts
    modules = {
        'organizations': {'file': 'server/tools_SDK_organizations.py', 'expected': 173},
        'appliance': {'file': 'server/tools_SDK_appliance.py', 'expected': 130},
        'wireless': {'file': 'server/tools_SDK_wireless.py', 'expected': 116},
        'networks': {'file': 'server/tools_SDK_networks.py', 'expected': 114},
        'switch': {'file': 'server/tools_SDK_switch.py', 'expected': 101},
        'sm': {'file': 'server/tools_SDK_sm.py', 'expected': 49},
        'camera': {'file': 'server/tools_SDK_camera.py', 'expected': 45},
        'devices': {'file': 'server/tools_SDK_devices.py', 'expected': 27},
        'cellularGateway': {'file': 'server/tools_SDK_cellularGateway.py', 'expected': 24},
        'sensor': {'file': 'server/tools_SDK_sensor.py', 'expected': 18},
        'licensing': {'file': 'server/tools_SDK_licensing.py', 'expected': 8},
        'insight': {'file': 'server/tools_SDK_insight.py', 'expected': 7},
        'administered': {'file': 'server/tools_SDK_administered.py', 'expected': 4}
    }
    
    dashboard = meraki.DashboardAPI(api_key='dummy', suppress_logging=True)
    total_official_tools = 0
    total_implemented_tools = 0
    all_passed = True
    results = []
    
    print("## 📊 MODULE VALIDATION RESULTS\n")
    
    for module_name, module_info in modules.items():
        print(f"### {module_name.upper()} MODULE")
        
        try:
            # Get official SDK methods
            sdk_module = getattr(dashboard, module_name)
            official_methods = []
            
            for name in dir(sdk_module):
                if not name.startswith('_') and callable(getattr(sdk_module, name)):
                    # Convert camelCase to snake_case
                    snake_case = name[0].lower()
                    for c in name[1:]:
                        if c.isupper():
                            snake_case += '_' + c.lower()
                        else:
                            snake_case += c
                    official_methods.append(snake_case)
            
            official_methods.sort()
            official_count = len(official_methods)
            total_official_tools += official_count
            
            # Get current implementation
            result = subprocess.run(['grep', '-c', '@app.tool', module_info['file']], 
                                  capture_output=True, text=True)
            implemented_count = int(result.stdout.strip()) if result.returncode == 0 else 0
            total_implemented_tools += implemented_count
            
            # Get tool names
            name_result = subprocess.run(['grep', '-o', 'name="[^"]*"', module_info['file']],
                                      capture_output=True, text=True)
            
            current_tools = []
            if name_result.returncode == 0:
                for line in name_result.stdout.strip().split('\\n'):
                    if line:
                        tool_name = line.split('"')[1]
                        current_tools.append(tool_name)
            
            current_tools.sort()
            
            # Compare sets
            official_set = set(official_methods)
            current_set = set(current_tools)
            
            extra_tools = current_set - official_set
            missing_tools = official_set - current_set
            
            # Check syntax
            syntax_result = subprocess.run(['python', '-m', 'py_compile', module_info['file']],
                                        capture_output=True)
            syntax_passed = syntax_result.returncode == 0
            
            # Determine pass/fail
            perfect_mapping = (official_count == implemented_count and 
                             not extra_tools and not missing_tools and syntax_passed)
            
            if perfect_mapping:
                status = "✅ PASS"
                print(f"   Status: {status}")
                print(f"   Tools: {implemented_count}/{official_count} (Perfect 1:1)")
                print(f"   Syntax: ✅ Clean")
            else:
                status = "❌ FAIL" 
                all_passed = False
                print(f"   Status: {status}")
                print(f"   Tools: {implemented_count}/{official_count}")
                print(f"   Expected: {module_info['expected']}")
                print(f"   Syntax: {'✅' if syntax_passed else '❌'}")
                
                if extra_tools:
                    print(f"   Extra: {len(extra_tools)} tools")
                    for tool in sorted(extra_tools)[:3]:
                        print(f"     - {tool}")
                    if len(extra_tools) > 3:
                        print(f"     ... and {len(extra_tools)-3} more")
                
                if missing_tools:
                    print(f"   Missing: {len(missing_tools)} tools")
                    for tool in sorted(missing_tools)[:3]:
                        print(f"     - {tool}")
                    if len(missing_tools) > 3:
                        print(f"     ... and {len(missing_tools)-3} more")
            
            results.append({
                'module': module_name,
                'status': status,
                'official': official_count,
                'implemented': implemented_count,
                'perfect': perfect_mapping,
                'extra': len(extra_tools),
                'missing': len(missing_tools)
            })
            
        except Exception as e:
            print(f"   Status: ❌ ERROR - {str(e)}")
            all_passed = False
            results.append({
                'module': module_name,
                'status': '❌ ERROR',
                'official': 0,
                'implemented': 0,
                'perfect': False,
                'extra': 0,
                'missing': 0
            })
        
        print()
    
    # Summary
    print("=" * 60)
    print("## 🏆 COMPREHENSIVE VALIDATION SUMMARY")
    print()
    
    passed_modules = [r for r in results if r['perfect']]
    failed_modules = [r for r in results if not r['perfect']]
    
    print(f"✅ **Passed Modules**: {len(passed_modules)}/13")
    print(f"❌ **Failed Modules**: {len(failed_modules)}/13")
    print(f"📊 **Total Official SDK Tools**: {total_official_tools}")
    print(f"📊 **Total Implemented Tools**: {total_implemented_tools}")
    print(f"🎯 **Coverage**: {(total_implemented_tools/total_official_tools)*100:.1f}%")
    
    if passed_modules:
        print(f"\\n### ✅ PASSED MODULES ({len(passed_modules)}):")
        for result in passed_modules:
            print(f"   • {result['module']}: {result['implemented']}/{result['official']} tools")
    
    if failed_modules:
        print(f"\\n### ❌ FAILED MODULES ({len(failed_modules)}):")
        for result in failed_modules:
            print(f"   • {result['module']}: {result['implemented']}/{result['official']} tools (+{result['extra']}/-{result['missing']})")
    
    # Final status
    if all_passed and total_implemented_tools == 816:
        print(f"\\n🎉 **FINAL STATUS: ALL MODULES PERFECT!**")
        print(f"🚀 **816 Official SDK Tools - 100% Coverage Achieved**")
        print(f"✅ **Perfect 1:1 mapping across all 13 modules**")
        print(f"📡 **Ready for production deployment**")
        return True
    else:
        print(f"\\n⚠️ **FINAL STATUS: ISSUES FOUND**")
        print(f"🔧 **Action Required**: Fix failing modules before deployment")
        return False

if __name__ == "__main__":
    success = validate_all_modules()
    print(f"\\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sys.exit(0 if success else 1)