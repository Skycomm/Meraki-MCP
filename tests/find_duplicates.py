#!/usr/bin/env python3
"""
Find duplicate tools in appliance file to clean up registrations.
"""

import re

def find_duplicates():
    """Find duplicate tool registrations."""
    
    with open('server/tools_SDK_appliance.py', 'r') as f:
        content = f.read()
    
    # Find all tool names with their line numbers
    lines = content.split('\n')
    tools = {}
    
    for i, line in enumerate(lines, 1):
        match = re.search(r'name="([^"]*)"', line)
        if match:
            tool_name = match.group(1)
            if tool_name not in tools:
                tools[tool_name] = []
            tools[tool_name].append(i)
    
    # Find duplicates
    print("# 🔍 Duplicate Tool Analysis\n")
    
    duplicates = {}
    for tool_name, line_numbers in tools.items():
        if len(line_numbers) > 1:
            duplicates[tool_name] = line_numbers
    
    print(f"**Total Tools Found**: {len(tools)}")
    print(f"**Duplicate Tools**: {len(duplicates)}")
    
    if duplicates:
        print(f"\n## 🚨 Duplicate Tools:")
        for tool_name, line_numbers in sorted(duplicates.items()):
            print(f"- **{tool_name}**: Lines {line_numbers}")
            
            # Determine which ones are in the final batch (5533+)
            final_batch_lines = [ln for ln in line_numbers if ln >= 5533]
            if final_batch_lines:
                print(f"  → Remove from lines: {final_batch_lines}")
    
    # Count tools before and after line 5533
    before_5533 = sum(1 for lines in tools.values() for ln in lines if ln < 5533)
    after_5533 = sum(1 for lines in tools.values() for ln in lines if ln >= 5533)
    
    print(f"\n## 📊 Tool Distribution:")
    print(f"- **Before line 5533**: {before_5533} tools")
    print(f"- **After line 5533**: {after_5533} tools")
    
    return duplicates

if __name__ == "__main__":
    duplicates = find_duplicates()