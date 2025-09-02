#!/usr/bin/env python3
"""
Final cleanup of all duplicate tools in appliance file.
"""

import re

def clean_all_duplicates():
    """Remove ALL duplicate tool definitions, keeping only the first occurrence of each."""
    
    with open('server/tools_SDK_appliance.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Track seen tool names and their line numbers
    seen_tools = {}
    tools_to_remove = []
    
    # Find all tool definitions
    for i, line in enumerate(lines):
        match = re.search(r'name="([^"]*)"', line)
        if match:
            tool_name = match.group(1)
            if tool_name in seen_tools:
                # This is a duplicate - find the complete function to remove
                start_line = i - 1  # Start from @app.tool line
                while start_line >= 0 and not lines[start_line].strip().startswith('@app.tool('):
                    start_line -= 1
                
                # Find end of function
                end_line = i + 1
                indent_level = len(lines[i]) - len(lines[i].lstrip())
                
                # Find the next function or end
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith('@app.tool(') or lines[j].strip().startswith('# Register'):
                        end_line = j - 1
                        break
                    elif j == len(lines) - 1:
                        end_line = j
                
                tools_to_remove.append((tool_name, start_line, end_line))
                print(f"Duplicate found: {tool_name} at lines {start_line+1}-{end_line+1}")
            else:
                seen_tools[tool_name] = i
    
    # Remove duplicates by excluding their line ranges
    cleaned_lines = []
    skip_until = -1
    
    for i, line in enumerate(lines):
        if i <= skip_until:
            continue
            
        # Check if this line starts a duplicate tool
        should_skip = False
        for tool_name, start_line, end_line in tools_to_remove:
            if i == start_line:
                print(f"Removing duplicate: {tool_name} (lines {start_line+1}-{end_line+1})")
                skip_until = end_line
                should_skip = True
                break
        
        if not should_skip:
            cleaned_lines.append(line)
    
    # Write cleaned content
    cleaned_content = '\n'.join(cleaned_lines)
    
    with open('server/tools_SDK_appliance.py', 'w') as f:
        f.write(cleaned_content)
    
    print(f"\n✅ Cleanup complete:")
    print(f"- Original lines: {len(lines)}")
    print(f"- Cleaned lines: {len(cleaned_lines)}")
    print(f"- Duplicates removed: {len(tools_to_remove)}")
    
    return len(tools_to_remove)

if __name__ == "__main__":
    removed = clean_all_duplicates()