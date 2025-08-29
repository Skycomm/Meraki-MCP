import re
import os

# Files to extract from
source_files = [
    '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_complete.py',
    '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_final.py',
    '/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_wireless_100.py',
]

# Tools we want for SSID features
ssid_feature_patterns = [
    'hotspot', 'splash', 'schedule', 'vpn', 'bonjour', 'eap_override',
    'device_type_group_policies', 'identity_psk'
]

tools_to_extract = []

for filepath in source_files:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Find all tool definitions
        tool_blocks = re.findall(r'@app\.tool\([^)]+\)\s+def\s+(\w+)\(', content, re.DOTALL)
        
        for tool_name in tool_blocks:
            for pattern in ssid_feature_patterns:
                if pattern in tool_name:
                    tools_to_extract.append(tool_name)
                    print(f"Found SSID feature tool: {tool_name}")
                    break

print(f"\nTotal SSID feature tools to extract: {len(set(tools_to_extract))}")
