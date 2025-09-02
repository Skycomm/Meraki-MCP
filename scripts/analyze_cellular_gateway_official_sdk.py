#!/usr/bin/env python3
"""
Analyze official Cisco Meraki cellular gateway SDK to identify exactly which 24 methods should exist.
Compare against current 32 tools to find the 8 extras to remove.
"""

import meraki

def analyze_cellular_gateway_sdk():
    """Get official cellular gateway SDK methods and compare with current implementation."""
    
    print("🔍 ANALYZING OFFICIAL CELLULAR GATEWAY SDK FOR CLEANUP\n")
    
    # Get official SDK methods
    print("## 📚 Extracting Official SDK Methods...")
    dashboard = meraki.DashboardAPI(api_key='dummy', suppress_logging=True)
    cellular_gateway = dashboard.cellularGateway
    
    official_methods = []
    for name in dir(cellular_gateway):
        if not name.startswith('_') and callable(getattr(cellular_gateway, name)):
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
                'callable': getattr(cellular_gateway, name)
            })
    
    official_methods.sort(key=lambda x: x['snake_case'])
    
    print(f"✅ Found {len(official_methods)} official SDK methods")
    print("\n## 🎯 Official SDK Methods (Target: 24 tools):")
    
    # Save official methods to file for comparison
    with open('/tmp/official_cellular_gateway_methods.txt', 'w') as f:
        for method in official_methods:
            print(f"   {method['snake_case']}")
            f.write(f"{method['snake_case']}\n")
    
    # Read current implementation
    print(f"\n## 🔍 Current Implementation Analysis...")
    import subprocess
    
    # Get current tool names from the cellular gateway module
    result = subprocess.run(['grep', '-o', 'name="[^"]*"', 'server/tools_SDK_cellularGateway.py'],
                          capture_output=True, text=True)
    
    current_tools = []
    if result.returncode == 0:
        for line in result.stdout.strip().split('\n'):
            if line:
                tool_name = line.split('"')[1]
                current_tools.append(tool_name)
    
    current_tools.sort()
    print(f"✅ Found {len(current_tools)} current tools")
    
    # Save current tools for comparison
    with open('/tmp/current_cellular_gateway_tools.txt', 'w') as f:
        for tool in current_tools:
            print(f"   {tool}")
            f.write(f"{tool}\n")
    
    # Find differences
    print(f"\n## 🧹 Cleanup Analysis:")
    official_set = set(method['snake_case'] for method in official_methods)
    current_set = set(current_tools)
    
    extra_tools = current_set - official_set
    missing_tools = official_set - current_set
    
    print(f"✅ Target: {len(official_methods)} official SDK tools")
    print(f"📊 Current: {len(current_tools)} tools")
    print(f"🧹 Need to remove: {len(extra_tools)} extra tools")
    print(f"➕ Need to add: {len(missing_tools)} missing tools")
    
    if extra_tools:
        print(f"\n### 🗑️ Extra Tools to Remove ({len(extra_tools)}):")
        for tool in sorted(extra_tools):
            print(f"   - {tool}")
    
    if missing_tools:
        print(f"\n### ➕ Missing Tools to Add ({len(missing_tools)}):")
        for tool in sorted(missing_tools):
            print(f"   - {tool}")
    
    # Summary
    cleanup_needed = len(extra_tools) - len(missing_tools)
    if cleanup_needed > 0:
        print(f"\n🎯 **CLEANUP SUMMARY**: Remove {cleanup_needed} tools ({len(current_tools)} → {len(official_methods)})")
    elif cleanup_needed < 0:
        print(f"\n🎯 **EXPANSION NEEDED**: Add {abs(cleanup_needed)} tools ({len(current_tools)} → {len(official_methods)})")
    else:
        print(f"\n✅ **PERFECT MATCH**: Already {len(official_methods)} tools")
    
    return {
        'official_methods': official_methods,
        'current_tools': current_tools,
        'extra_tools': extra_tools,
        'missing_tools': missing_tools,
        'cleanup_needed': cleanup_needed
    }

if __name__ == "__main__":
    result = analyze_cellular_gateway_sdk()
    print(f"\n🏁 Analysis complete! Check /tmp/official_cellular_gateway_methods.txt and /tmp/current_cellular_gateway_tools.txt")