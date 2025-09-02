#!/usr/bin/env python3
"""
Clean duplicate tools from appliance file by removing those in the final batch (5533+).
"""

import re

def clean_duplicates():
    """Remove duplicate tools from final batch."""
    
    with open('server/tools_SDK_appliance.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Tools to remove (duplicates from final batch that exist earlier)
    duplicates_to_remove = [
        "get_network_appliance_firewall_settings",  # line 6271
        "swap_network_appliance_warm_spare",       # line 5653
        "update_network_appliance_firewall_one_to_one_nat_rules",  # line 6013
        "update_network_appliance_firewall_port_forwarding_rules", # line 6035
        "update_network_appliance_firewall_settings",              # line 6291
        "update_network_appliance_security_intrusion",             # line 6091
        "update_network_appliance_security_malware",               # line 6057
        "update_network_appliance_traffic_shaping_uplink_selection" # line 5770
    ]
    
    print("# 🧹 Cleaning Duplicate Tools\n")
    
    # Track which tools we're removing and their line ranges
    tools_to_remove = {}
    
    # Find the complete function definitions to remove
    for i, line in enumerate(lines):
        # Look for tool decorators in final batch (line 5533+)
        if i >= 5532:  # 0-based indexing, so 5532 = line 5533
            match = re.search(r'name="([^"]*)"', line)
            if match:
                tool_name = match.group(1)
                if tool_name in duplicates_to_remove:
                    # Find the start of this tool (decorator line)
                    decorator_line = i
                    
                    # Find the end of this tool (next decorator or end)
                    end_line = len(lines) - 1
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip().startswith('@app.tool(') or lines[j].strip().startswith('# Register additional'):
                            end_line = j - 1
                            break
                    
                    tools_to_remove[tool_name] = (decorator_line, end_line)
                    print(f"Found duplicate: {tool_name} (lines {decorator_line+1}-{end_line+1})")
    
    print(f"\n**Tools to remove**: {len(tools_to_remove)}")
    
    # Remove the tools by marking lines for deletion
    lines_to_keep = []
    skip_until = -1
    
    for i, line in enumerate(lines):
        if i <= skip_until:
            continue
            
        # Check if this line starts a tool we want to remove
        should_skip = False
        for tool_name, (start_line, end_line) in tools_to_remove.items():
            if i == start_line:
                print(f"Removing {tool_name} (lines {start_line+1}-{end_line+1})")
                skip_until = end_line
                should_skip = True
                break
        
        if not should_skip:
            lines_to_keep.append(line)
    
    # Write cleaned content
    cleaned_content = '\n'.join(lines_to_keep)
    
    with open('server/tools_SDK_appliance.py', 'w') as f:
        f.write(cleaned_content)
    
    print(f"\n✅ **Cleanup Complete**")
    print(f"**Lines before**: {len(lines)}")
    print(f"**Lines after**: {len(lines_to_keep)}")
    print(f"**Lines removed**: {len(lines) - len(lines_to_keep)}")
    
    return len(tools_to_remove)

if __name__ == "__main__":
    removed_count = clean_duplicates()