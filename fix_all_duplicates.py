#!/usr/bin/env python3
"""Fix all duplicate tool registrations across the codebase."""

import os
import re

def comment_out_functions(filepath, function_names, explanation):
    """Comment out specific functions in a file."""
    if not os.path.exists(filepath):
        print(f"  ⚠️ File not found: {filepath}")
        return 0
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    changes_made = 0
    
    for func_name in function_names:
        # Find the decorator and function definition
        pattern = rf'(\n    @app\.tool\([^)]*name="{func_name}"[^)]*\)[^)]*\n    def {func_name}\([^)]*\):)'
        
        if re.search(pattern, content, re.MULTILINE | re.DOTALL):
            # Find complete function including body
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
            if match:
                start = match.start()
                
                # Find the end of the function
                next_decorator = content.find('\n    @app.tool(', start + 1)
                next_def = content.find('\n    def ', start + len(match.group(0)) + 1)
                end_of_register = content.find('\ndef register_', start + 1)
                
                # Determine the end position
                end_positions = [pos for pos in [next_decorator, next_def, end_of_register, len(content)] if pos > start]
                end = min(end_positions)
                
                # Extract the function
                func_content = content[start:end]
                
                # Comment it out
                commented = f"\n    # {explanation}\n"
                lines = func_content.split('\n')[1:]  # Skip first empty line
                commented += '\n'.join('    # ' + line if line.strip() else '    #' for line in lines)
                
                # Replace in content
                content = content[:start] + commented + content[end:]
                changes_made += 1
                print(f"  ✓ Commented out {func_name}")
    
    if changes_made > 0:
        with open(filepath, 'w') as f:
            f.write(content)
    
    return changes_made

def main():
    """Fix all duplicate tool registrations."""
    print("=" * 60)
    print("Fixing All Duplicate Tool Registrations")
    print("=" * 60)
    
    fixes = [
        # Analytics has duplicate uplink status from appliance
        {
            'file': 'server/tools_analytics.py',
            'functions': ['get_organization_appliance_uplink_statuses'],
            'explanation': 'DUPLICATE - Already in tools_appliance.py'
        },
        # Beta has early access which is in dedicated module
        {
            'file': 'server/tools_beta.py',
            'functions': ['get_organization_early_access_features'],
            'explanation': 'DUPLICATE - Already in tools_early_access.py'
        },
        # Organizations additional has early access too
        {
            'file': 'server/tools_organizations_additional.py',
            'functions': ['get_organization_early_access_features'],
            'explanation': 'DUPLICATE - Already in tools_early_access.py'
        },
        # Switch has DHCP policy which is in dedicated module
        {
            'file': 'server/tools_switch.py',
            'functions': [
                'get_network_switch_dhcp_server_policy',
                'update_network_switch_dhcp_server_policy'
            ],
            'explanation': 'DUPLICATE - Already in tools_switch_dhcp_policy.py'
        },
        # Monitoring dashboard has uplink status and health summary duplicates
        {
            'file': 'server/tools_monitoring_dashboard.py',
            'functions': [
                'get_organization_appliance_uplink_statuses',
                'get_network_health_summary'
            ],
            'explanation': 'DUPLICATE - Already in tools_appliance.py and tools_networks.py'
        }
    ]
    
    total_fixed = 0
    
    for fix in fixes:
        print(f"\nProcessing {fix['file']}...")
        count = comment_out_functions(fix['file'], fix['functions'], fix['explanation'])
        total_fixed += count
    
    print("\n" + "=" * 60)
    print(f"✅ Fixed {total_fixed} duplicate tool registrations")
    print("=" * 60)
    
    # Test imports to ensure no syntax errors
    print("\nTesting imports...")
    try:
        import sys
        sys.path.insert(0, 'server')
        from main import app
        print("✅ All modules import successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")

if __name__ == "__main__":
    main()