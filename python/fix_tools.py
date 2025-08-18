#!/usr/bin/env python3
"""Fix indentation issues in meraki_tools.py"""

import re

# Read the file
with open('src/meraki_tools.py', 'r') as f:
    content = f.read()

# Fix the specific pattern where try/except blocks are incorrectly indented
# Look for patterns where 'try:' appears after function definition
lines = content.split('\n')
fixed_lines = []
in_function = False
base_indent = 0

for i, line in enumerate(lines):
    # Detect function definition
    if line.startswith('async def '):
        in_function = True
        base_indent = 0
        fixed_lines.append(line)
        continue
    
    # Handle the line after function definition
    if in_function and i > 0 and lines[i-1].startswith('async def '):
        fixed_lines.append(line)
        continue
        
    # Handle 'if not meraki_client:' line
    if in_function and 'if not meraki_client:' in line:
        fixed_lines.append(line)
        continue
        
    # Handle the return after 'if not meraki_client:'
    if in_function and i > 0 and 'if not meraki_client:' in lines[i-1]:
        fixed_lines.append(line)
        continue
    
    # If we see a try: that's not properly indented
    if in_function and line.strip() == 'try:':
        fixed_lines.append('    try:')
        base_indent = 8  # Set base indent for try block
        continue
    
    # If we see except after try
    if in_function and line.strip().startswith('except'):
        fixed_lines.append('    ' + line.strip())
        base_indent = 8  # Set base indent for except block
        continue
    
    # If we're in a try/except block, ensure proper indentation
    if in_function and base_indent > 0 and line.strip():
        # Count current indentation
        current_indent = len(line) - len(line.lstrip())
        
        # If line is less indented than expected, it might be end of function
        if current_indent < 4 and not line.startswith('async def'):
            in_function = False
            base_indent = 0
            fixed_lines.append(line)
        else:
            # Ensure minimum indentation
            if current_indent < base_indent:
                fixed_lines.append(' ' * base_indent + line.strip())
            else:
                fixed_lines.append(line)
    else:
        fixed_lines.append(line)
        
    # Reset when we see a new function
    if line.strip() == '' and i + 1 < len(lines) and lines[i+1].startswith('async def'):
        in_function = False
        base_indent = 0

# Write the fixed content
with open('src/meraki_tools.py', 'w') as f:
    f.write('\n'.join(fixed_lines))

print("Fixed indentation issues")