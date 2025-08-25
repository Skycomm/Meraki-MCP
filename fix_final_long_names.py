#!/usr/bin/env python3
"""Fix all remaining tool names that exceed 64 characters."""

import re
import os

def shorten_name(name):
    """Shorten a tool name to fit within 64 characters."""
    if len(name) <= 64:
        return name
    
    # Strategy: Remove less important words and abbreviate
    replacements = [
        ('organization', 'org'),
        ('appliance', 'app'),
        ('network', 'net'),
        ('traffic_shaping', 'ts'),
        ('custom_performance_class', 'cpc'),
        ('firewall', 'fw'),
        ('inbound_cellular', 'cell_in'),
        ('application_categories', 'app_cats'),
        ('inventory_onboarding_cloud_monitoring', 'inv_cloud_mon'),
        ('packet_capture_capture', 'pcap'),
        ('api_requests_overview_response_codes', 'api_resp_codes'),
        ('assignments_bulk', 'bulk'),
        ('multicast_forwarding', 'mcast_fwd'),
        ('vpn_exclusions', 'vpn_excl'),
        ('dns_local_profiles', 'dns_local'),
        ('dns_split_profiles', 'dns_split'),
    ]
    
    shortened = name
    for old, new in replacements:
        shortened = shortened.replace(old, new)
        if len(shortened) <= 64:
            break
    
    return shortened

def fix_long_names_in_file(filepath):
    """Fix long tool names in a single file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all tool name declarations
    pattern = r'(@app\.tool\([^)]*name="([^"]+)")'
    
    changes_made = []
    def replace_long_name(match):
        full_match = match.group(1)
        name = match.group(2)
        
        if len(name) > 64:
            new_name = shorten_name(name)
            changes_made.append((name, new_name))
            return full_match.replace(f'name="{name}"', f'name="{new_name}"')
        return full_match
    
    new_content = re.sub(pattern, replace_long_name, content)
    
    if changes_made:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"\n{filepath}:")
        for old, new in changes_made:
            print(f"  {old} ({len(old)} chars)")
            print(f"  -> {new} ({len(new)} chars)")
    
    return len(changes_made)

def main():
    """Fix all long tool names."""
    print("=" * 60)
    print("Fixing Tool Names Longer Than 64 Characters")
    print("=" * 60)
    
    total_fixed = 0
    
    # Process all tools files
    for filename in os.listdir('server'):
        if filename.startswith('tools_') and filename.endswith('.py'):
            filepath = os.path.join('server', filename)
            count = fix_long_names_in_file(filepath)
            total_fixed += count
    
    print("\n" + "=" * 60)
    print(f"✅ Fixed {total_fixed} long tool names")
    print("=" * 60)

if __name__ == "__main__":
    main()