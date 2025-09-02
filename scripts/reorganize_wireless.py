#!/usr/bin/env python3
"""
Reorganize wireless tools into logical files.
This extracts tool functions and reorganizes them.
"""

import re
import os

def extract_tool_function(content, tool_name):
    """Extract a complete tool function from content."""
    # Find the @app.tool decorator and the function
    pattern = rf'(@app\.tool\([^)]+\)\s+def\s+{tool_name}\([^)]*\):[^@]*?)(?=@app\.tool|def register_|$)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_imports(content):
    """Extract import statements."""
    imports = []
    for line in content.split('\n'):
        if line.startswith('from ') or line.startswith('import '):
            if line not in imports:
                imports.append(line)
    return imports

# Read all source files
source_files = {
    'complete': '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_complete.py',
    'final': '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_final.py',
    'hundred': '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_100.py',
    'missing': '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_missing.py',
    'advanced': '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_advanced.py',
    'firewall': '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_firewall.py',
    'rf': '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_rf_profiles.py',
}

file_contents = {}
for name, path in source_files.items():
    if os.path.exists(path):
        with open(path, 'r') as f:
            file_contents[name] = f.read()

# Define tool categories and their patterns
categories = {
    'ssid_features': {
        'patterns': ['hotspot', 'splash', 'schedule', 'vpn', 'bonjour', 'eap_override', 
                    'device_type_group_policies', 'identity_psk'],
        'tools': []
    },
    'security': {
        'patterns': ['firewall', 'air_marshal', 'traffic_shaping', 'isolation_allowlist'],
        'tools': []
    },
    'analytics': {
        'patterns': ['connection_stats', 'latency_stats', 'latency_history', 'failed_connections',
                    'health_scores', 'usage_history', 'data_rate_history', 'signal_quality',
                    'client_count_history', 'channel_utilization_history'],
        'tools': []
    },
    'infrastructure': {
        'patterns': ['bluetooth', 'electronic_shelf', 'ethernet_ports', 'alternate_management',
                    'location_scanning', 'billing'],
        'tools': []
    },
    'organization': {
        'patterns': ['organization_wireless', 'packet_loss', 'power_mode', 'cpu_load',
                    'radsec', 'wireless_controllers'],
        'tools': []
    },
    'rf': {
        'patterns': ['rf_profile', 'radio_settings', 'mesh_status', 'channel_utilization'],
        'tools': []
    }
}

# Find all tools and categorize them
all_tools = {}
for name, content in file_contents.items():
    # Find all tool names in this file
    tool_names = re.findall(r'@app\.tool\([^)]+\)\s+def\s+(\w+)\(', content, re.DOTALL)
    
    for tool_name in tool_names:
        # Skip if already processed
        if tool_name in all_tools:
            continue
            
        # Categorize the tool
        categorized = False
        for cat_name, cat_info in categories.items():
            for pattern in cat_info['patterns']:
                if pattern in tool_name.lower():
                    cat_info['tools'].append(tool_name)
                    all_tools[tool_name] = (name, cat_name)
                    categorized = True
                    break
            if categorized:
                break
        
        if not categorized:
            print(f"Uncategorized tool: {tool_name} from {name}")

# Report findings
print("=" * 60)
print("REORGANIZATION PLAN")
print("=" * 60)

for cat_name, cat_info in categories.items():
    print(f"\n{cat_name}: {len(cat_info['tools'])} tools")
    for tool in cat_info['tools'][:5]:
        source_file = all_tools.get(tool, ('unknown', ''))[0]
        print(f"  - {tool} (from {source_file})")
    if len(cat_info['tools']) > 5:
        print(f"  ... and {len(cat_info['tools']) - 5} more")

print(f"\nTotal tools to reorganize: {len(all_tools)}")
print("\nReady to create reorganized files!")
