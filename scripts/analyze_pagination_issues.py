#!/usr/bin/env python3
"""
Analyze pagination issues across all MCP SDK tools.
"""

import os
import re
import sys

def analyze_tool_files():
    """Analyze all SDK tool files for pagination issues."""
    
    # Get all SDK tool files
    tool_files = []
    server_dir = 'server'
    
    for file in os.listdir(server_dir):
        if file.startswith('tools_SDK_') and file.endswith('.py'):
            tool_files.append(os.path.join(server_dir, file))
    
    print(f"🔍 ANALYZING {len(tool_files)} SDK MODULES FOR PAGINATION ISSUES")
    print("=" * 70)
    
    total_tools = 0
    problematic_tools = 0
    fixes_needed = []
    
    for file_path in tool_files:
        module_name = os.path.basename(file_path).replace('tools_SDK_', '').replace('.py', '')
        print(f"\\n### {module_name.upper()} MODULE")
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find all @app.tool definitions
        tool_pattern = r'@app\.tool\(.*?name="([^"]+)".*?\).*?def ([^(]+)\([^)]*per_page[^)]*\):'
        tools_with_per_page = re.findall(tool_pattern, content, re.DOTALL)
        
        # Count total tools in file
        total_tools_in_file = len(re.findall(r'@app\.tool\(', content))
        total_tools += total_tools_in_file
        
        if tools_with_per_page:
            print(f"   📊 Total tools: {total_tools_in_file}")
            print(f"   ❌ Tools with per_page: {len(tools_with_per_page)}")
            problematic_tools += len(tools_with_per_page)
            
            # Show first few problematic tools
            for i, (tool_name, func_name) in enumerate(tools_with_per_page[:3]):
                print(f"      - {tool_name} ({func_name})")
            
            if len(tools_with_per_page) > 3:
                print(f"      ... and {len(tools_with_per_page) - 3} more")
            
            fixes_needed.append({
                'module': module_name,
                'file': file_path,
                'tools': tools_with_per_page
            })
        else:
            print(f"   ✅ All {total_tools_in_file} tools clean (no per_page issues)")
    
    print("\\n" + "=" * 70)
    print("🏆 SUMMARY")
    print("=" * 70)
    print(f"📊 **Total Tools Analyzed**: {total_tools}")
    print(f"❌ **Tools with per_page issues**: {problematic_tools}")
    print(f"✅ **Tools working correctly**: {total_tools - problematic_tools}")
    print(f"📁 **Modules needing fixes**: {len(fixes_needed)}")
    
    if fixes_needed:
        print("\\n🔧 **MODULES REQUIRING PAGINATION FIXES**:")
        for fix in fixes_needed:
            print(f"   - {fix['module']}: {len(fix['tools'])} tools")
    
    return fixes_needed

def generate_fix_recommendations():
    """Generate specific fix recommendations."""
    print("\\n" + "=" * 70)
    print("💡 FIX RECOMMENDATIONS")
    print("=" * 70)
    
    print("""
**RECOMMENDED APPROACH:**

1. **Quick Fix Pattern** (for most tools):
   ```python
   # Before (❌):
   def tool(network_id: str, per_page: int = 1000):
       kwargs = {"perPage": per_page} if "per_page" in locals() else {}
       result = method(network_id, **kwargs)
   
   # After (✅):
   def tool(network_id: str):
       result = method(network_id)
   ```

2. **For methods needing timespan**:
   ```python
   def tool(network_id: str, timespan: int = 86400):
       result = method(network_id, timespan=timespan)
   ```

3. **For methods needing organization pagination**:
   ```python  
   def tool(org_id: str, total_pages: int = 1):
       result = method(org_id, total_pages=total_pages)
   ```

**PRIORITY:**
- High: wireless, networks, organizations (user-facing)
- Medium: appliance, switch (infrastructure)  
- Low: camera, sensor, insight (specialized)
""")

if __name__ == "__main__":
    if not os.path.exists('server'):
        print("❌ Run this script from the project root directory")
        sys.exit(1)
    
    fixes_needed = analyze_tool_files()
    generate_fix_recommendations()
    
    print(f"\\n🎯 **NEXT STEP**: Fix {len(fixes_needed)} modules systematically")