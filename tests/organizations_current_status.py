#!/usr/bin/env python3
"""
Check current status of organizations module vs official SDK.
"""

import subprocess
import re

def check_organizations_status():
    """Check current organizations module status."""
    
    print("# 🏢 Organizations Module Status Check\n")
    
    # Get current tool count
    result = subprocess.run(['grep', '-c', '@app.tool(', 'server/tools_SDK_organizations.py'], 
                          capture_output=True, text=True)
    current_count = int(result.stdout.strip()) if result.returncode == 0 else 0
    
    print(f"## 📊 Current Status")
    print(f"- **Current Tools**: {current_count}")
    print(f"- **Target (Official SDK)**: 173")
    print(f"- **Progress**: {(current_count/173)*100:.1f}%")
    print(f"- **Gap**: {173 - current_count} tools missing\n")
    
    # Check for duplicates
    with open('server/tools_SDK_organizations.py', 'r') as f:
        content = f.read()
    
    # Extract all tool names
    tool_names = re.findall(r'name="([^"]*)"', content)
    
    # Find duplicates
    from collections import Counter
    name_counts = Counter(tool_names)
    duplicates = {name: count for name, count in name_counts.items() if count > 1}
    
    if duplicates:
        print(f"## ⚠️ Duplicates Found ({len(duplicates)} tools)")
        for name, count in sorted(duplicates.items()):
            print(f"- **{name}**: {count} instances")
        print()
    else:
        print("## ✅ No Duplicates Found\n")
    
    # Compare naming patterns
    org_names = [name for name in tool_names if '_org_' in name and name not in duplicates]
    organization_names = [name for name in tool_names if '_organization_' in name and name not in duplicates]
    
    print(f"## 🏷️ Naming Patterns")
    print(f"- **Short form** (`_org_`): {len(org_names)} tools")
    print(f"- **Long form** (`_organization_`): {len(organization_names)} tools")
    print(f"- **Mixed naming**: {'⚠️ Inconsistent' if org_names and organization_names else '✅ Consistent'}\n")
    
    if org_names and organization_names:
        print("### Short Form Examples:")
        for name in sorted(org_names)[:5]:
            print(f"- {name}")
        print("\n### Long Form Examples:")
        for name in sorted(organization_names)[:5]:
            print(f"- {name}")
        print()
    
    # Check syntax
    syntax_check = subprocess.run(['python', '-m', 'py_compile', 'server/tools_SDK_organizations.py'], 
                                capture_output=True)
    
    print(f"## 🔧 Technical Status")
    print(f"- **Syntax**: {'✅ Clean' if syntax_check.returncode == 0 else '❌ Errors found'}")
    print(f"- **File Size**: {len(content)} characters")
    print(f"- **Total Lines**: {len(content.splitlines())}")
    
    if syntax_check.returncode != 0:
        print(f"- **Syntax Error**: {syntax_check.stderr.decode()[:200]}...")
    
    print()
    
    # Recommendations
    print("## 💡 Recommended Actions")
    
    if duplicates:
        print("1. **Remove Duplicates**: Clean up duplicate tool definitions")
    
    if org_names and organization_names:
        print("2. **Standardize Naming**: Choose consistent naming pattern")
        
    remaining = 173 - len(set(tool_names))  # Unique tools
    if remaining > 0:
        print(f"3. **Add Missing Tools**: {remaining} more tools needed for 100% SDK coverage")
    
    if remaining == 0 and not duplicates:
        print("🎉 **Ready for final verification!**")
    
    return {
        'current_count': current_count,
        'unique_count': len(set(tool_names)),
        'duplicates': len(duplicates),
        'target': 173,
        'remaining': max(0, 173 - len(set(tool_names)))
    }

if __name__ == "__main__":
    status = check_organizations_status()