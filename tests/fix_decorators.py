#!/usr/bin/env python3
"""
Fix duplicate @app.tool decorators in appliance file.
"""

def fix_decorators():
    """Remove duplicate @app.tool decorators."""
    
    with open('server/tools_SDK_appliance.py', 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # If this is an @app.tool decorator
        if line.strip() == '@app.tool(':
            fixed_lines.append(line)
            i += 1
            
            # Skip any immediate duplicate @app.tool decorators
            while i < len(lines) and lines[i].strip() == '@app.tool(':
                print(f"Removing duplicate @app.tool at line {i+1}")
                i += 1
                
        else:
            fixed_lines.append(line)
            i += 1
    
    # Write the fixed content
    with open('server/tools_SDK_appliance.py', 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed decorators. Lines: {len(lines)} -> {len(fixed_lines)}")

if __name__ == "__main__":
    fix_decorators()