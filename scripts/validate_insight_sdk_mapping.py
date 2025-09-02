#!/usr/bin/env python3
"""
Validate that Insight module has perfect 1:1 mapping with official SDK.
"""

import meraki
import subprocess

def validate_insight_sdk_mapping():
    """Validate insight module has perfect 1:1 SDK mapping."""
    
    print("🔍 VALIDATING INSIGHT MODULE 1:1 SDK MAPPING\n")
    
    # Get official SDK methods
    print("## 📚 Extracting Official SDK Methods...")
    dashboard = meraki.DashboardAPI(api_key='dummy', suppress_logging=True)
    insight = dashboard.insight
    
    official_methods = []
    for name in dir(insight):
        if not name.startswith('_') and callable(getattr(insight, name)):
            # Convert camelCase to snake_case
            snake_case = name[0].lower()
            for c in name[1:]:
                if c.isupper():
                    snake_case += '_' + c.lower()
                else:
                    snake_case += c
            
            official_methods.append({
                'original': name,
                'snake_case': snake_case,
                'callable': getattr(insight, name)
            })
    
    official_methods.sort(key=lambda x: x['snake_case'])
    print(f"✅ Found {len(official_methods)} official SDK methods")
    
    # List all official methods
    print("\n### Official SDK Methods:")
    for method in official_methods:
        print(f"   {method['snake_case']}")
    
    # Get current implementation
    print(f"\n## 🔍 Current Implementation Analysis...")
    result = subprocess.run(['grep', '-o', 'name="[^"]*"', 'server/tools_SDK_insight.py'],
                          capture_output=True, text=True)
    
    current_tools = []
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            if line:
                tool_name = line.split('"')[1]
                current_tools.append(tool_name)
    
    current_tools.sort()
    print(f"✅ Found {len(current_tools)} current tools")
    
    # List all current tools
    print("\n### Current Tools:")
    for tool in current_tools:
        print(f"   {tool}")
    
    # Compare
    print(f"\n## 🧹 Mapping Analysis:")
    official_set = set(method['snake_case'] for method in official_methods)
    current_set = set(current_tools)
    
    extra_tools = current_set - official_set
    missing_tools = official_set - current_set
    
    print(f"✅ Target: {len(official_methods)} official SDK tools")
    print(f"📊 Current: {len(current_tools)} tools")
    
    if extra_tools:
        print(f"\n### 🗑️ Extra Tools ({len(extra_tools)}):")
        for tool in sorted(extra_tools):
            print(f"   - {tool}")
    
    if missing_tools:
        print(f"\n### ➕ Missing Tools ({len(missing_tools)}):")
        for tool in sorted(missing_tools):
            print(f"   - {tool}")
    
    # Final assessment
    if len(official_methods) == len(current_tools) and not extra_tools and not missing_tools:
        print(f"\n✅ **PERFECT 1:1 MAPPING**: Insight module is correctly implemented")
        return True
    else:
        print(f"\n⚠️ **MAPPING MISMATCH**: Insight module needs cleanup")
        print(f"   • Need to remove: {len(extra_tools)} extra tools")
        print(f"   • Need to add: {len(missing_tools)} missing tools")
        return False

if __name__ == "__main__":
    success = validate_insight_sdk_mapping()
    print(f"\n🏁 Insight validation: {'PASSED' if success else 'FAILED'}")