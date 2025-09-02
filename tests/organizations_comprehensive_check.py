#!/usr/bin/env python3
"""
Comprehensive verification of Organizations SDK coverage.
Maps each official SDK method to implemented tools and shows exactly what's missing.
"""

import meraki
import re
import subprocess

def comprehensive_organizations_check():
    """Comprehensive check of organizations module against official SDK."""
    
    print("# 🎯 COMPREHENSIVE ORGANIZATIONS SDK VERIFICATION\n")
    
    # Get official SDK methods
    print("## 📚 Getting Official SDK Methods...")
    try:
        dashboard = meraki.DashboardAPI(api_key='dummy', suppress_logging=True)
        orgs = dashboard.organizations
        
        official_methods = []
        for name in dir(orgs):
            if not name.startswith('_') and callable(getattr(orgs, name)):
                # Convert to snake_case for MCP tool names
                snake_case = name[0].lower()
                for c in name[1:]:
                    if c.isupper():
                        snake_case += '_' + c.lower()
                    else:
                        snake_case += c
                official_methods.append(snake_case)
        
        official_methods.sort()
        print(f"✅ Found {len(official_methods)} official SDK methods\n")
        
    except Exception as e:
        print(f"❌ Error getting SDK methods: {e}")
        return False
    
    # Get current implemented tools
    print("## 🔍 Analyzing Current Implementation...")
    try:
        with open('server/tools_SDK_organizations.py', 'r') as f:
            content = f.read()
        
        # Extract tool names
        tool_names = re.findall(r'name="([^"]*)"', content)
        implemented_tools = sorted(set(tool_names))  # Remove duplicates
        
        print(f"✅ Found {len(implemented_tools)} implemented tools")
        print(f"📊 Raw count (with duplicates): {len(tool_names)}")
        if len(tool_names) != len(implemented_tools):
            print(f"⚠️ Duplicates found: {len(tool_names) - len(implemented_tools)}")
        print()
        
    except Exception as e:
        print(f"❌ Error reading organizations file: {e}")
        return False
    
    # Create mapping between official methods and implemented tools
    print("## 🗺️ SDK Method Mapping\n")
    
    mapped_tools = set()
    missing_methods = []
    extra_tools = []
    
    # Check each official method
    for method in official_methods:
        found = False
        
        # Look for exact match first
        if method in implemented_tools:
            mapped_tools.add(method)
            found = True
        else:
            # Check for common variations
            variations = [
                method,
                method.replace('_organization_', '_org_'),  # Short form
                method.replace('organization_', 'org_'),     # Even shorter
            ]
            
            for variation in variations:
                if variation in implemented_tools:
                    mapped_tools.add(variation)
                    found = True
                    break
        
        if not found:
            missing_methods.append(method)
    
    # Find extra tools not in official SDK
    for tool in implemented_tools:
        if tool not in mapped_tools:
            # Check if it's a variation of an official method
            is_variation = False
            original_form = tool.replace('_org_', '_organization_')
            if original_form.startswith('org_'):
                original_form = 'organization_' + original_form[4:]
            
            if original_form in official_methods:
                is_variation = True
                mapped_tools.add(tool)
            
            if not is_variation:
                extra_tools.append(tool)
    
    # Results
    print(f"### ✅ Successfully Mapped: {len(mapped_tools)}/173 ({(len(mapped_tools)/173)*100:.1f}%)")
    print(f"### ❌ Missing Methods: {len(missing_methods)}")
    print(f"### ➕ Extra Tools: {len(extra_tools)}")
    print()
    
    # Show missing methods
    if missing_methods:
        print("## 🚫 Missing SDK Methods (Need Implementation):")
        for i, method in enumerate(missing_methods[:20], 1):
            print(f"{i:2d}. {method}")
        if len(missing_methods) > 20:
            print(f"    ... and {len(missing_methods)-20} more")
        print()
    
    # Show extra tools
    if extra_tools:
        print("## ➕ Extra Tools (Not in Official SDK):")
        for i, tool in enumerate(extra_tools[:10], 1):
            print(f"{i:2d}. {tool}")
        if len(extra_tools) > 10:
            print(f"    ... and {len(extra_tools)-10} more")
        print()
    
    # Check syntax
    print("## 🔧 Technical Validation")
    syntax_result = subprocess.run(['python', '-m', 'py_compile', 'server/tools_SDK_organizations.py'],
                                 capture_output=True)
    
    if syntax_result.returncode == 0:
        print("✅ **Syntax**: Clean, no errors")
    else:
        print("❌ **Syntax**: Errors found")
        print(f"   Error: {syntax_result.stderr.decode()[:100]}...")
    
    # Final assessment
    print("\\n## 🎯 Final Assessment")
    
    coverage_percent = (len(mapped_tools) / 173) * 100
    
    if len(mapped_tools) == 173 and syntax_result.returncode == 0:
        print("🎉 **MISSION ACCOMPLISHED: ORGANIZATIONS MODULE COMPLETE!**")
        print(f"🏆 **100% Cisco Meraki Organizations SDK Coverage Achieved**")
        print(f"📡 **Ready for production use with Claude Desktop**")
    else:
        print(f"📊 **Status**: {coverage_percent:.1f}% complete")
        if missing_methods:
            print(f"⚠️ **Action Required**: Implement {len(missing_methods)} missing methods")
        if syntax_result.returncode != 0:
            print("⚠️ **Action Required**: Fix syntax errors")
    
    return {
        'mapped_tools': len(mapped_tools),
        'missing_methods': len(missing_methods),
        'extra_tools': len(extra_tools),
        'coverage_percent': coverage_percent,
        'syntax_clean': syntax_result.returncode == 0
    }

if __name__ == "__main__":
    result = comprehensive_organizations_check()