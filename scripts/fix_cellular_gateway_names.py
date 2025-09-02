#!/usr/bin/env python3
"""
Fix cellular gateway tool names that exceed 64 characters for MCP compliance.
"""

import re

def fix_cellular_gateway_names():
    """Fix tool names that exceed 64-character MCP limit."""
    
    print("🔧 FIXING CELLULAR GATEWAY TOOL NAMES FOR MCP COMPLIANCE\n")
    
    # Read current file
    with open('server/tools_SDK_cellularGateway.py', 'r') as f:
        content = f.read()
    
    # Define name mappings (original -> shortened)
    name_mappings = {
        # 65+ chars -> <64 chars
        'create_organization_cellular_gateway_esims_service_providers_account': 'create_org_cg_esims_service_provider_account',
        'delete_organization_cellular_gateway_esims_service_providers_account': 'delete_org_cg_esims_service_provider_account', 
        'get_network_cellular_gateway_connectivity_monitoring_destinations': 'get_network_cg_connectivity_monitoring_destinations',
        'get_organization_cellular_gateway_esims_service_providers_accounts': 'get_org_cg_esims_service_provider_accounts',
        'get_organization_cellular_gateway_esims_service_providers_accounts_communication_plans': 'get_org_cg_esims_service_provider_comm_plans',
        'get_organization_cellular_gateway_esims_service_providers_accounts_rate_plans': 'get_org_cg_esims_service_provider_rate_plans',
        'update_network_cellular_gateway_connectivity_monitoring_destinations': 'update_network_cg_connectivity_monitoring_dest',
        'update_organization_cellular_gateway_esims_service_providers_account': 'update_org_cg_esims_service_provider_account'
    }
    
    print("## 🏷️ Applying Name Mappings...")
    changes_made = 0
    
    for original_name, shortened_name in name_mappings.items():
        print(f"   {original_name} -> {shortened_name} ({len(original_name)} -> {len(shortened_name)} chars)")
        
        # Replace in name declarations
        old_name_pattern = f'name="{original_name}"'
        new_name_pattern = f'name="{shortened_name}"'
        if old_name_pattern in content:
            content = content.replace(old_name_pattern, new_name_pattern)
            changes_made += 1
        
        # Replace in function definitions
        old_func_pattern = f'def {original_name}('
        new_func_pattern = f'def {shortened_name}('
        if old_func_pattern in content:
            content = content.replace(old_func_pattern, new_func_pattern)
            changes_made += 1
        
        # Replace in error messages
        old_error_pattern = f'Error in {original_name}:'
        new_error_pattern = f'Error in {shortened_name}:'
        if old_error_pattern in content:
            content = content.replace(old_error_pattern, new_error_pattern)
            changes_made += 1
    
    print(f"✅ Applied {changes_made} name changes")
    
    # Write back the fixed content
    with open('server/tools_SDK_cellularGateway.py', 'w') as f:
        f.write(content)
    
    print("\\n## 🔍 Verifying Name Lengths...")
    
    # Verify all names are now compliant
    import subprocess
    name_result = subprocess.run(['grep', '-o', 'name="[^"]*"', 'server/tools_SDK_cellularGateway.py'], 
                                capture_output=True, text=True)
    
    if name_result.returncode == 0:
        tool_names = []
        for line in name_result.stdout.strip().split('\\n'):
            if line:
                name = line.split('"')[1]
                tool_names.append(name)
        
        long_names = [name for name in tool_names if len(name) > 64]
        
        if long_names:
            print(f"⚠️ Still found {len(long_names)} names exceeding 64 chars:")
            for name in long_names:
                print(f"   - {name} ({len(name)} chars)")
            return False
        else:
            print(f"✅ All {len(tool_names)} tool names now comply with 64-character limit")
            
            # Show shortest and longest names for reference
            shortest = min(tool_names, key=len)
            longest = max(tool_names, key=len)
            print(f"   Shortest: {shortest} ({len(shortest)} chars)")
            print(f"   Longest: {longest} ({len(longest)} chars)")
    
    # Test syntax
    print("\\n## 🧪 Testing Syntax...")
    syntax_result = subprocess.run(['python', '-m', 'py_compile', 'server/tools_SDK_cellularGateway.py'],
                                 capture_output=True)
    
    if syntax_result.returncode == 0:
        print("✅ Syntax check passed!")
        return True
    else:
        print(f"❌ Syntax error: {syntax_result.stderr.decode()[:200]}")
        return False

if __name__ == "__main__":
    success = fix_cellular_gateway_names()
    print(f"\\n🏁 Name fix: {'SUCCESS' if success else 'FAILED'}")