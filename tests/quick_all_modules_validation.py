#!/usr/bin/env python3
"""
Quick validation test - just verify tool counts and syntax for all modules.
"""

import subprocess
import sys
from datetime import datetime

def quick_validate_all_modules():
    """Quick validation of all 13 SDK modules - counts and syntax only."""
    
    print("🔍 QUICK ALL MODULES VALIDATION")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Define all SDK modules with expected counts
    modules = {
        'Organizations': {'file': 'server/tools_SDK_organizations.py', 'expected': 173},
        'Appliance': {'file': 'server/tools_SDK_appliance.py', 'expected': 130},
        'Wireless': {'file': 'server/tools_SDK_wireless.py', 'expected': 116},
        'Networks': {'file': 'server/tools_SDK_networks.py', 'expected': 114},
        'Switch': {'file': 'server/tools_SDK_switch.py', 'expected': 101},
        'SM': {'file': 'server/tools_SDK_sm.py', 'expected': 49},
        'Camera': {'file': 'server/tools_SDK_camera.py', 'expected': 45},
        'Devices': {'file': 'server/tools_SDK_devices.py', 'expected': 27},
        'Cellular Gateway': {'file': 'server/tools_SDK_cellularGateway.py', 'expected': 24},
        'Sensor': {'file': 'server/tools_SDK_sensor.py', 'expected': 18},
        'Licensing': {'file': 'server/tools_SDK_licensing.py', 'expected': 8},
        'Insight': {'file': 'server/tools_SDK_insight.py', 'expected': 7},
        'Administered': {'file': 'server/tools_SDK_administered.py', 'expected': 4}
    }
    
    total_expected = sum(m['expected'] for m in modules.values())
    total_actual = 0
    all_passed = True
    
    print("## 📊 MODULE VALIDATION RESULTS\n")
    
    for module_name, module_info in modules.items():
        # Count @app.tool decorators
        count_result = subprocess.run(['grep', '-c', '@app.tool', module_info['file']], 
                                    capture_output=True, text=True)
        actual_count = int(count_result.stdout.strip()) if count_result.returncode == 0 else 0
        total_actual += actual_count
        
        # Check syntax
        syntax_result = subprocess.run(['python', '-m', 'py_compile', module_info['file']],
                                     capture_output=True)
        syntax_passed = syntax_result.returncode == 0
        
        # Determine status
        count_perfect = actual_count == module_info['expected']
        module_passed = count_perfect and syntax_passed
        
        if not module_passed:
            all_passed = False
        
        status = "✅ PASS" if module_passed else "❌ FAIL"
        
        print(f"**{module_name}**: {status}")
        print(f"   Tools: {actual_count}/{module_info['expected']} {'✅' if count_perfect else '❌'}")
        print(f"   Syntax: {'✅' if syntax_passed else '❌'}")
        
        if not syntax_passed:
            error_msg = syntax_result.stderr.decode()[:100]
            print(f"   Error: {error_msg}...")
        
        print()
    
    # Summary
    print("=" * 50)
    print("## 🏆 VALIDATION SUMMARY")
    print()
    
    print(f"📊 **Total Expected Tools**: {total_expected}")
    print(f"📊 **Total Actual Tools**: {total_actual}")
    print(f"🎯 **Count Match**: {'✅' if total_actual == total_expected else '❌'}")
    print(f"🎯 **All Modules Pass**: {'✅' if all_passed else '❌'}")
    
    if total_actual == 816 and all_passed:
        print(f"\\n🎉 **FINAL STATUS: ALL MODULES PERFECT!**")
        print(f"🚀 **816 Official SDK Tools - Ready for Production**")
        print(f"✅ **All syntax checks pass**")
        print(f"📡 **Ready for MCP server startup test**")
        return True
    else:
        print(f"\\n⚠️ **FINAL STATUS: ISSUES FOUND**")
        if total_actual != 816:
            print(f"🔧 **Tool Count Issue**: Expected 816, got {total_actual}")
        if not all_passed:
            print(f"🔧 **Module Issues**: Some modules have syntax or count problems")
        return False

if __name__ == "__main__":
    success = quick_validate_all_modules()
    print(f"\\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sys.exit(0 if success else 1)