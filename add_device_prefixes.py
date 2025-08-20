#!/usr/bin/env python3
"""
Add device type prefixes to tool names for better discovery.
This script analyzes tools and suggests appropriate prefixes.
"""

import os
import re
import glob

# Device type mappings
DEVICE_PREFIXES = {
    'appliance': '[MX]',
    'switch': '[MS]',
    'wireless': '[MR]',
    'camera': '[MV]',
    'sm': '[SM]',
    'cellularGateway': '[MG]',
    'sensor': '[MT]',
    'all': '[ALL]'
}

# Keywords to identify device types
DEVICE_KEYWORDS = {
    'appliance': ['firewall', 'vpn', 'dhcp', 'uplink', 'wan', 'security', 'intrusion', 'traffic_shaping', 'port_forward'],
    'switch': ['switch', 'port', 'vlan', 'stp', 'storm', 'cable_test', 'mac_table'],
    'wireless': ['wireless', 'ssid', 'wifi', 'radio', 'rf', 'mesh', 'bluetooth'],
    'camera': ['camera', 'video', 'motion', 'snapshot', 'recording'],
    'sm': ['mdm', 'mobile', 'device_management', 'profile', 'app_management'],
    'cellularGateway': ['cellular', 'gateway', 'sim', 'uplink_cellular'],
    'sensor': ['sensor', 'temperature', 'humidity', 'water', 'door', 'environmental']
}

def identify_device_type(tool_name, description=""):
    """Identify device type based on tool name and description."""
    combined = f"{tool_name} {description}".lower()
    
    # Check each device type
    matches = []
    for device_type, keywords in DEVICE_KEYWORDS.items():
        if any(keyword in combined for keyword in keywords):
            matches.append(device_type)
    
    # Return most specific match or 'all' if multiple or none
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        # Prioritize more specific types
        if 'appliance' in matches and any(kw in combined for kw in ['firewall', 'vpn', 'dhcp']):
            return 'appliance'
        elif 'switch' in matches and any(kw in combined for kw in ['switch', 'port']):
            return 'switch'
        elif 'wireless' in matches and any(kw in combined for kw in ['wireless', 'ssid', 'wifi']):
            return 'wireless'
    
    # Default to 'all' for generic tools
    return 'all'

def analyze_tools():
    """Analyze all tool files and suggest prefixes."""
    tool_files = glob.glob('/Users/david/docker/cisco-meraki-mcp-server-tvi/server/tools_*.py')
    
    suggestions = []
    
    for tool_file in sorted(tool_files):
        with open(tool_file, 'r') as f:
            content = f.read()
        
        # Find all tool definitions
        tool_pattern = r'@(?:mcp_)?app\.tool\(\s*(?:name\s*=\s*"([^"]+)")?.*?\)\s*def\s+(\w+)'
        tools = re.findall(tool_pattern, content, re.DOTALL)
        
        # Also find simple def patterns
        simple_pattern = r'def\s+((?:get|set|update|create|delete|list|check|analyze|diagnose|configure|generate|schedule|track|export|manage|add|remove)\w+)\s*\('
        simple_tools = re.findall(simple_pattern, content)
        
        if tools or simple_tools:
            filename = os.path.basename(tool_file)
            suggestions.append(f"\n## {filename}")
            
            # Process found tools
            all_tools = []
            for tool in tools:
                tool_name = tool[0] if tool[0] else tool[1]
                all_tools.append(tool_name)
            
            all_tools.extend(simple_tools)
            
            # Remove duplicates
            all_tools = list(set(all_tools))
            
            for tool_name in sorted(all_tools):
                # Skip help functions
                if 'help' in tool_name.lower():
                    continue
                    
                device_type = identify_device_type(tool_name, filename)
                prefix = DEVICE_PREFIXES[device_type]
                
                suggestions.append(f"- {tool_name} → {prefix} {tool_name}")
    
    return suggestions

def main():
    """Main function to analyze and display suggestions."""
    print("🔍 Analyzing tools for device type prefixes...\n")
    
    suggestions = analyze_tools()
    
    print("📋 Suggested Tool Prefixes:")
    print("=" * 60)
    
    for suggestion in suggestions:
        print(suggestion)
    
    print("\n💡 Implementation Plan:")
    print("1. Update tool names in registration")
    print("2. Add prefixes to help text")
    print("3. Update documentation")
    print("4. Test tool discovery")
    
    print("\n📊 Prefix Guide:")
    for device_type, prefix in DEVICE_PREFIXES.items():
        print(f"   {prefix} - {device_type.title()} tools")

if __name__ == "__main__":
    main()