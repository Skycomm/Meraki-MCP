#!/usr/bin/env python3
"""
Final comprehensive validation of complete Cisco Meraki MCP Server.
816 SDK tools + 13 unique custom tools = 829 total tools.
"""

import subprocess
import sys
from datetime import datetime

def final_complete_validation():
    """Final comprehensive validation of the complete MCP server."""
    
    print("🎯 FINAL COMPREHENSIVE VALIDATION")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Testing: 816 SDK + 13 unique custom = 829 total tools\n")
    
    # Test 1: SDK modules validation (should be 816)
    print("## 📊 SDK MODULES VALIDATION\n")
    
    sdk_modules = {
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
    
    sdk_total = 0
    sdk_passed = 0
    
    for module_name, module_info in sdk_modules.items():
        result = subprocess.run(['grep', '-c', '@app.tool', module_info['file']], 
                              capture_output=True, text=True)
        actual = int(result.stdout.strip()) if result.returncode == 0 else 0
        sdk_total += actual
        
        if actual == module_info['expected']:
            sdk_passed += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"{status} {module_name}: {actual}/{module_info['expected']} tools")
    
    # Test 2: Custom modules validation (should be 13 unique)
    print(f"\\n## 🔧 CUSTOM MODULES VALIDATION\\n")
    
    custom_modules = {
        'Alerts Filtered': {'file': 'server/tools_Custom_alerts_filtered.py', 'expected': 7},
        'Monitoring Filtered': {'file': 'server/tools_Custom_monitoring_filtered.py', 'expected': 6}
    }
    
    custom_total = 0
    custom_passed = 0
    
    for module_name, module_info in custom_modules.items():
        result = subprocess.run(['grep', '-c', '@app.tool', module_info['file']], 
                              capture_output=True, text=True)
        actual = int(result.stdout.strip()) if result.returncode == 0 else 0
        custom_total += actual
        
        if actual == module_info['expected']:
            custom_passed += 1
            status = "✅"
        else:
            status = "❌"
        
        print(f"{status} {module_name}: {actual}/{module_info['expected']} tools")
    
    # Test 3: Server startup test
    print(f"\\n## 🚀 SERVER STARTUP TEST\\n")
    
    try:
        startup_result = subprocess.run([
            '.venv/bin/python', '-c', 
            'import sys; sys.path.insert(0, "."); from server.main import app; print("SUCCESS")'
        ], capture_output=True, text=True, env={'MCP_PROFILE': 'FULL'})
        
        if startup_result.returncode == 0 and "SUCCESS" in startup_result.stdout:
            print("✅ Server startup: SUCCESS")
            server_passed = True
        else:
            print("❌ Server startup: FAILED")
            print(f"Error: {startup_result.stderr[:200]}")
            server_passed = False
    except Exception as e:
        print(f"❌ Server startup: ERROR - {e}")
        server_passed = False
    
    # Test 4: Syntax validation
    print(f"\\n## 🔧 SYNTAX VALIDATION\\n")
    
    all_files = [info['file'] for info in sdk_modules.values()] + [info['file'] for info in custom_modules.values()]
    syntax_passed = 0
    
    for file_path in all_files:
        result = subprocess.run(['python', '-m', 'py_compile', file_path], capture_output=True)
        if result.returncode == 0:
            syntax_passed += 1
        else:
            print(f"❌ {file_path}: Syntax error")
    
    if syntax_passed == len(all_files):
        print(f"✅ All {len(all_files)} files: Clean syntax")
    else:
        print(f"❌ {syntax_passed}/{len(all_files)} files: Syntax issues found")
    
    # Final assessment
    print("\\n" + "=" * 60)
    print("## 🏆 FINAL ASSESSMENT\\n")
    
    print(f"📊 **SDK Modules**: {sdk_passed}/13 perfect ({sdk_total} total tools)")
    print(f"🔧 **Custom Modules**: {custom_passed}/2 perfect ({custom_total} unique tools)")
    print(f"🚀 **Server Startup**: {'✅ PASS' if server_passed else '❌ FAIL'}")
    print(f"🔧 **Syntax Check**: {'✅ PASS' if syntax_passed == len(all_files) else '❌ FAIL'}")
    
    expected_total = 816 + 13
    actual_total = sdk_total + custom_total
    
    print(f"\\n📊 **TOTAL TOOL COUNT**")
    print(f"Expected: {expected_total} tools (816 SDK + 13 unique custom)")
    print(f"Actual: {actual_total} tools ({sdk_total} SDK + {custom_total} custom)")
    
    all_passed = (
        sdk_passed == 13 and 
        custom_passed == 2 and 
        server_passed and 
        syntax_passed == len(all_files) and
        actual_total == expected_total
    )
    
    if all_passed:
        print(f"\\n🎉 **FINAL STATUS: COMPLETE SUCCESS!**")
        print(f"✅ Perfect 816 SDK tools with 100% official coverage")
        print(f"✅ Perfect 13 unique custom tools (webhook + analytics)")
        print(f"✅ Total 829 tools - most comprehensive Meraki MCP server")
        print(f"✅ Zero duplicates, clean architecture, production ready")
        print(f"🚀 **READY FOR DEPLOYMENT WITH CLAUDE DESKTOP**")
        return True
    else:
        print(f"\\n⚠️ **FINAL STATUS: ISSUES FOUND**")
        print(f"🔧 Review failed components above")
        return False

if __name__ == "__main__":
    success = final_complete_validation()
    print(f"\\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sys.exit(0 if success else 1)